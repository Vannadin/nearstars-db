// YZ Cet b의 별-행성 자기 플럭스 튜브를 ScaledSpace에 LineRenderer로 그리는 KSP 플러그인 (프로토타입 스켈레톤)
using System;
using UnityEngine;

namespace NearStars.FluxTube
{
    // 비행/우주센터/맵에서 살아있도록. 트래킹 스테이션에서도 보이게 하려면
    // KSPAddon을 하나 더(Startup.TrackingStation) 두거나 EveryScene으로 바꾸면 됨.
    [KSPAddon(KSPAddon.Startup.FlightAndKSC, false)]
    public class FluxTubeRenderer : MonoBehaviour
    {
        // ---- 설정값 (추후 GameDatabase로 .cfg에서 읽어오게 바꿀 자리) ----
        const string StarName   = "YZCet";   // Kopernicus 시스템에서의 CelestialBody.name
        const string PlanetName = "YZCetb";
        const int    Segments   = 96;         // 곡선 분할 수
        const float  BowHeight  = 0.45f;      // 활이 바깥으로 부푸는 정도(별-행성 거리 대비)
        const float  WidthFrac  = 0.012f;     // 튜브 두께(별 반지름 대비)
        const double ScrollSpeed= 0.15;       // 텍스처 흐름 속도
        static readonly Color AuroraColor = new Color(0.25f, 0.90f, 0.70f, 1f);

        CelestialBody star, planet;
        LineRenderer  line;
        Material      mat;
        readonly Vector3[] pts = new Vector3[Segments + 1];

        void Start()
        {
            star   = FindBody(StarName);
            planet = FindBody(PlanetName);
            if (star == null || planet == null)
            {
                Debug.LogWarning($"[NS-FluxTube] body not found ({StarName}/{PlanetName}) — disabling.");
                enabled = false;
                return;
            }
            BuildLine();
        }

        static CelestialBody FindBody(string name)
        {
            foreach (var b in FlightGlobals.Bodies)
                if (b != null && b.name == name) return b;
            return null;
        }

        void BuildLine()
        {
            var go = new GameObject("NS_FluxTube");
            go.layer = 10; // ScaledSpace 레이어 → 행성 스케일(맵/원거리)에서 렌더됨

            line = go.AddComponent<LineRenderer>();
            line.positionCount    = pts.Length;
            line.useWorldSpace    = true;   // 매 프레임 ScaledSpace 좌표를 직접 먹임
            line.numCapVertices   = 6;      // 끝을 둥글게
            line.numCornerVertices= 4;
            line.alignment        = LineAlignment.View; // 항상 카메라를 향하는 빌보드 튜브

            mat = new Material(FindGlowShader());
            // 가산 합성 셰이더는 텍스처가 있어야 보임. 없으면 부드러운 흰 스트립을 생성.
            mat.mainTexture = MakeSoftStripTexture();
            line.material = mat;

            // 양 극(발자국)이 가장 밝고, 중심으로 갈수록 옅어지는 알파 그라데이션
            var grad = new Gradient();
            grad.SetKeys(
                new[] { new GradientColorKey(AuroraColor, 0f),
                        new GradientColorKey(AuroraColor, 1f) },
                new[] { new GradientAlphaKey(1.0f,  0f),    // 별 극 발자국
                        new GradientAlphaKey(0.5f,  0.18f),
                        new GradientAlphaKey(0.06f, 0.5f),  // 중심 = 거의 투명(가는 실만)
                        new GradientAlphaKey(0.5f,  0.82f),
                        new GradientAlphaKey(1.0f,  1f) });  // 행성 극 발자국
            line.colorGradient = grad;
        }

        void LateUpdate()
        {
            if (line == null) return;

            // --- 양 끝점: 각 천체의 자기 극(자전축으로 근사) ---
            // bodyTransform.up = 자전(북극) 축. 반지름만큼 밀면 극점 위치.
            Vector3d starPole   = star.position   + (Vector3d)star.bodyTransform.up   * star.Radius;
            Vector3d planetPole = planet.position + (Vector3d)planet.bodyTransform.up * planet.Radius;

            // --- 쌍극자처럼 바깥으로 부푸는 베지어 제어점 ---
            Vector3d mid     = (starPole + planetPole) * 0.5;
            double   dist    = (planetPole - starPole).magnitude;
            Vector3d outward = (mid - star.position).normalized;        // 별 중심 반대 방향으로 부풀림
            Vector3d apex    = mid + outward * (dist * BowHeight);
            Vector3d c1      = Vector3d.Lerp(starPole,   apex, 0.5);
            Vector3d c2      = Vector3d.Lerp(planetPole, apex, 0.5);

            // --- 베지어 샘플링 → 각 점을 ScaledSpace로 변환 ---
            for (int i = 0; i <= Segments; i++)
            {
                double t = (double)i / Segments;
                pts[i] = ScaledSpace.LocalToScaledSpace(Bezier(starPole, c1, c2, planetPole, t));
            }
            line.SetPositions(pts);

            // --- 두께(ScaledSpace 단위) ---
            float w = (float)(star.Radius * WidthFrac / ScaledSpace.ScaleFactor);
            line.startWidth = line.endWidth = w;

            // --- 행성 공전 위상에 밝기를 키잉 (= SPI 버스트가 공전 위상 따라가는 그 물리) ---
            double phase = planet.orbit != null ? planet.orbit.trueAnomaly : 0.0;
            float  pulse = 0.4f + 0.6f * (0.5f + 0.5f * (float)Math.Cos(phase));
            Color  c = AuroraColor * pulse; c.a = 1f;
            mat.SetColor("_TintColor", c); // Particles/Additive 계열은 _TintColor 사용

            // --- 텍스처를 튜브 따라 흘려서 흐르는 느낌 ---
            float off = -(float)((Planetarium.GetUniversalTime() * ScrollSpeed) % 1.0);
            mat.mainTextureOffset = new Vector2(off, 0f);
        }

        static Vector3d Bezier(Vector3d p0, Vector3d p1, Vector3d p2, Vector3d p3, double t)
        {
            double u = 1.0 - t;
            return u*u*u*p0 + 3*u*u*t*p1 + 3*u*t*t*p2 + t*t*t*p3;
        }

        static Shader FindGlowShader()
        {
            // Unity 버전별로 경로가 달라 후보를 순서대로 시도.
            string[] names = { "KSP/Particles/Additive",
                               "Legacy Shaders/Particles/Additive",
                               "Particles/Additive" };
            foreach (var n in names)
            {
                var s = Shader.Find(n);
                if (s != null) return s;
            }
            return Shader.Find("Sprites/Default"); // 최후 폴백
        }

        static Texture2D MakeSoftStripTexture()
        {
            // 가운데가 밝고 가장자리가 옅은 1×N 세로 스트립(튜브 단면 글로우용).
            const int n = 32;
            var tex = new Texture2D(1, n, TextureFormat.ARGB32, false) { wrapMode = TextureWrapMode.Repeat };
            for (int y = 0; y < n; y++)
            {
                float d = Mathf.Abs(y - (n - 1) * 0.5f) / ((n - 1) * 0.5f); // 0=중앙, 1=가장자리
                float a = Mathf.Clamp01(1f - d * d);
                tex.SetPixel(0, y, new Color(1f, 1f, 1f, a));
            }
            tex.Apply();
            return tex;
        }

        void OnDestroy()
        {
            if (line != null) Destroy(line.gameObject);
            if (mat  != null) Destroy(mat);
        }
    }
}
