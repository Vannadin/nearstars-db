# 7900X 데스크탑에서 stability-sim 돌리기 — WSL2 셋업 (짧은 버전)

Windows 네이티브는 REBOUND(C 확장)를 못 빌드한다. WSL2(Windows 안의 리눅스)를 쓰면 24스레드를 그대로 다 쓴다. 병렬 스윕 전용 — 장시간 단일 적분은 Mac이 유리.

## 1. WSL2 설치 (PowerShell **관리자**로)

```powershell
wsl --install        # Ubuntu 기본 설치 + WSL2
# 재부팅 → Ubuntu 창이 뜨면 username/password 설정
```

## 2. Ubuntu 안에서 도구 설치

```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git build-essential
```

## 3. repo 가져오기

origin 에 이미 푸시돼 있으니 clone (git 인증 필요 — PAT 또는 ssh key):

```bash
git clone <NearStars repo URL> ~/NearStars
cd ~/NearStars
```

> 미커밋 변경(j2.py 등)은 그 세션에서 아직 없을 수 있다. clone 후 `git pull`로 최신 맞출 것. 또는 Windows 파일시스템의 repo를 `/mnt/c/...`로 접근해도 되지만, 빌드는 WSL 네이티브 경로(`~/`)가 빠르다.

## 4. venv + rebound

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install rebound==5.0.0      # reboundx 설치 금지 (rebound 5.x 호환판 없음 → 다운그레이드 사고)
.venv/bin/python -c "import rebound; print(rebound.__version__)"   # 5.0.0 확인
```

## 5. 스모크 확인

```bash
.venv/bin/python phase3/stability-sim/scripts/run.py --system alpha_centauri \
  --hypotheticals phase3/stability-sim/hypotheticals/alpha_centauri.json \
  --acen-a-au 1.6 --acen-e 0.1 --acen-incl-deg 16 --integrator trace \
  --years 50 --snapshots 10 --j2 0.023 --out /tmp/smoke
```

정상이면 5위성 a/e + bound=True 가 찍힌다. 이후 병렬 스윕은 `inclination_scan.py` / `cotilt_scan.py` 의 `WORKERS` 를 ~22 로 올려 24스레드 활용.

## 핵심 주의

- **reboundx 설치 금지** (rebound 을 4.x 로 다운그레이드시켜 named-particle API 전부 깨짐). J2 는 `scripts/j2.py` 가 자체 구현.
- J2 런은 IAS15 금지(Python 콜백 ×12 호출로 11배 느림) → `trace` 사용. 스캔 스크립트는 `STAB_J2` 켜지면 자동 trace.
- 작업은 worktree 로 격리, 공유 main 트리 switch/reset 금지 (다중 세션).
