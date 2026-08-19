/* J2 편평도 섭동 — j2.py 의 파이썬 콜백과 같은 식을 C 로 옮긴 것. 매 스텝 호출되므로
   파이썬 경계를 넘지 않는 것이 전부다(측정: 파이썬 콜백이 69배 느렸다).

   rebound 의 additional_forces 는 (struct reb_simulation*) 하나를 받는다. 우리는 그
   구조체 전체를 알 필요가 없고 particles 포인터와 개수만 있으면 되지만, 오프셋을 손으로
   맞추는 것은 버전이 바뀌면 조용히 틀어진다. 그래서 파라미터(축·계수·대상 인덱스)는
   파이썬이 setup 으로 미리 넣어두고, 힘 함수는 rebound 가 넘겨주는 시뮬레이션에서
   particles 배열만 헤더로 얻는다. */
#include <math.h>
#include <stdlib.h>

/* rebound 의 입자 구조체 앞부분 — x..az 까지는 5.x/4.x 모두 동일한 선두 배치다.
   뒤쪽 필드는 건드리지 않으므로 선언하지 않는다. */
struct particle_head {
    double x, y, z;
    double vx, vy, vz;
    double ax, ay, az;
    double m;
};

static double AX, AY, AZ;      /* 자전축 단위벡터 */
static double J2, REQ2;        /* J2, 적도반경^2 */
static double GRAV;            /* G */
static int    BODY;            /* 편평 천체 인덱스 */
static int   *MOONS;           /* 대상 위성 인덱스 */
static int    NMOON;

void ns_j2_setup(double ax, double ay, double az, double j2, double r_eq,
                 double g, int body, int *moons, int nmoon) {
    double n = sqrt(ax * ax + ay * ay + az * az);
    AX = ax / n; AY = ay / n; AZ = az / n;
    J2 = j2; REQ2 = r_eq * r_eq; GRAV = g;
    BODY = body; NMOON = nmoon;
    free(MOONS);
    MOONS = (int *)malloc(sizeof(int) * (size_t)nmoon);
    for (int i = 0; i < nmoon; i++) MOONS[i] = moons[i];
}

/* rebound 는 콜백에 시뮬레이션 포인터를 준다. particles 배열 포인터를 파이썬이
   ns_j2_bind 로 미리 알려주므로, 콜백은 구조체 레이아웃에 의존하지 않는다. */
static struct particle_head **PARTS;

void ns_j2_bind(struct particle_head **particles_ptr) { PARTS = particles_ptr; }

void ns_j2_force(void *sim) {
    (void)sim;
    struct particle_head *ps = *PARTS;
    struct particle_head *pl = &ps[BODY];
    const double mu = GRAV * pl->m;
    const double c0 = 1.5 * J2 * mu * REQ2;
    const double px = pl->x, py = pl->y, pz = pl->z;
    double rbx = 0.0, rby = 0.0, rbz = 0.0;

    for (int k = 0; k < NMOON; k++) {
        struct particle_head *m = &ps[MOONS[k]];
        const double dx = m->x - px, dy = m->y - py, dz = m->z - pz;
        const double r2 = dx * dx + dy * dy + dz * dz;
        const double r = sqrt(r2);
        const double zeta = dx * AX + dy * AY + dz * AZ;
        const double zr = zeta / r;
        const double common = c0 / (r2 * r2);
        const double f_rhat = 1.0 - 5.0 * zr * zr;
        const double amx = -common * (f_rhat * dx / r + 2.0 * zr * AX);
        const double amy = -common * (f_rhat * dy / r + 2.0 * zr * AY);
        const double amz = -common * (f_rhat * dz / r + 2.0 * zr * AZ);
        m->ax += amx; m->ay += amy; m->az += amz;
        rbx += m->m * amx; rby += m->m * amy; rbz += m->m * amz;
    }
    if (pl->m > 0.0) {
        pl->ax -= rbx / pl->m;
        pl->ay -= rby / pl->m;
        pl->az -= rbz / pl->m;
    }
}
