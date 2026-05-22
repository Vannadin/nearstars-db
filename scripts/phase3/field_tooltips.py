# Phase 3 Decisions 표 필드명 한글 호버 툴팁 사전
"""Korean tooltip text for standard cfg field names that appear in
Decisions tables and prose. Loaded by build_html.py to wrap `<code>...</code>`
blocks whose content matches a known field with a `.field-tt` span.

The tooltip appears on mouse hover only — no on-page legend per user request.
"""

FIELD_TOOLTIPS_KO: dict[str, str] = {
    # ── Orbital ────────────────────────────────────────────────────────────
    'tidally_locked':              '조석 고정 여부. 행성이 모항성에 한 면만 보임 (true/false).',
    'obliquity_deg':               '자전축 기울기 (도). 지구 ≈ 23.5°.',
    'eccentricity':                '궤도 이심률. 0 = 정원, 1 = 포물선.',
    'argument_of_periastron_deg':  '근일점 인수 (도). 궤도면 위 근일점 방향.',
    'sidereal_period_days':        '항성일 기준 자전 주기 (일).',
    'semi_major_axis_au':          '궤도 긴반지름 (AU, 1 AU = 지구–태양 거리).',
    'inclination_deg':             '시선 방향에 대한 궤도면 기울기 (도).',

    # ── Physical ───────────────────────────────────────────────────────────
    'mass_mearth':                 '질량 (지구질량 단위).',
    'radius_rearth':               '반지름 (지구반지름 단위).',
    'surface_gravity_g_earth':     '표면 중력 (지구 중력 1.0 단위).',
    'density_g_cc':                '평균 밀도 (g/cm³). 지구 ≈ 5.5.',
    'insolation_s_earth':          '항성으로부터 받는 복사 (지구 일조량 단위).',
    'equilibrium_temp_k':          '평형 온도 (K). 대기·온실효과 없이 흡수-방사 균형 가정.',
    'bond_albedo':                 '본드 반사율. 전 파장 통합 반사율 (0–1).',
    'water_mass_fraction':         '물 질량 분율. 지구 ≈ 0.0002.',

    # ── Atmosphere ─────────────────────────────────────────────────────────
    'atmosphere_present':          '대기 존재 여부 (true/false 또는 정성 표현).',
    'atmosphere_surface_pressure_pa': '표면 대기압 (Pa). 1 bar = 100,000 Pa.',
    'atmosphere_composition':      '대기 조성 (주 성분과 분압 비율).',
    'atmosphere_scale_height_km':  '대기 스케일 높이 (km). 압력이 1/e 로 떨어지는 고도.',
    'atmosphere_tint_rgb_hex':     '대기 limb (가장자리) 색조 hex.',
    'cloud_cover_fraction':        '구름 피복률 (0–1).',
    'cloud_morphology':            '구름 형태 (위도/경도 패턴 서술).',
    'cloud_tint_rgb_hex':          '구름 색조 hex.',

    # ── Surface ────────────────────────────────────────────────────────────
    'dayside_surface_temp_k':      '주간면 표면 온도 (K).',
    'nightside_surface_temp_k':    '야간면 표면 온도 (K).',
    'surface_temp_substellar_k':   'substellar (모항성 직하점) 표면 온도 (K).',
    'surface_temp_nightside_k':    '야간면 표면 온도 (K).',
    'surface_temp_global_mean_k':  '전구 평균 표면 온도 (K).',
    'dayside_brightness_temp_k':   'JWST 등에서 측정한 주간면 밝기 온도 (K, 파장대별).',
    'surface_tint_rgb_hex_primary': '표면 주 색조 hex.',
    'surface_tint_rgb_hex_accent': '표면 보조 색조 hex (스팟·패치).',
    'surface_morphology':          '표면 지형 서술 (크레이터·용암류·빙하 등).',
    'surface_ice_caps':            '극관·전구 빙상 분포.',
    'ocean_present':               '표면 액체수 해양 존재 여부.',
    'ocean_extent_substellar_radius_deg': 'substellar 지점 중심 열대 호수 반경 (도).',
    'ocean_tint_rgb_hex':          '해양 색조 hex.',

    # ── Interior heating ───────────────────────────────────────────────────
    'tidal_heating_w_m2':          '조석 가열 표면 flux (W/m²). Io ≈ 2.',
    'induction_heating_w_m2':      '항성 자기장 유도 가열 (W/m²).',
    'radiogenic_heat_w_m2':        '방사성 동위원소 붕괴 열 (W/m²). 지구 ≈ 0.087.',

    # ── Stellar / sky ──────────────────────────────────────────────────────
    'star_apparent_angular_diameter_deg': '하늘에서 모항성의 시직경 (도). 지구에서 본 태양 ≈ 0.53°.',
    'stellar_illumination_color_temp_k': '모항성 색온도 (K). 태양 ≈ 5778, M dwarf ≈ 2500-3500.',
    'xuv_flux_at_planet_F_earth':  '행성에 도달하는 XUV flux (지구 단위).',
    'stellar_microflare_cadence_min': '미세 플레어 평균 발생 간격 (분).',

    # ── Kerbalism (radiation / magnetosphere) ──────────────────────────────
    'magnetic_field_present':      '전구 자기장 (다이나모) 존재 여부.',
    'magnetic_field_strength_microtesla_equator': '적도 자기장 강도 (μT). 지구 ≈ 30.',
    'magnetic_dipole_moment_normalized_earth': '쌍극자 모멘트 (지구 = 1.0 단위).',
    'magnetic_dipole_tilt_deg':    '자전축에 대한 쌍극자 기울기 (도). 지구 ≈ 11°.',
    'magnetosphere_standoff_planet_radii': '자기권 standoff 거리 (행성반지름 단위).',
    'radiation_belt_present':      '밴 앨런 형 방사선대 존재 여부.',
    'radiation_inner_belt_radius_planet_radii': '내부 방사선대 반경 (행성반지름 단위).',
    'radiation_outer_belt_radius_planet_radii': '외부 방사선대 반경 (행성반지름 단위).',
    'surface_radiation_dose_msv_yr': '표면 연간 방사선량 (mSv/yr). 지구 ≈ 2.4.',
    'atmospheric_shielding_g_cm2': '대기 차폐량 (g/cm²). 지구 ≈ 1030.',

    # ── EVE (aurora) ───────────────────────────────────────────────────────
    'aurora_present':              '오로라 발생 여부 (대기 + 자기장 동시 필요).',
    'aurora_color_primary_hex':    '주 오로라 색 hex. 발광 종(species) 에 의해 결정.',
    'aurora_color_secondary_hex':  '보조 오로라 색 hex.',
    'aurora_emission_species_primary': '주 발광 종 (e.g. [OI] 557 nm, CO₂⁺ FDB).',
    'aurora_oval_magnetic_latitude_deg': '오로라 오벌 중심 자기 위도 (도). 지구 ≈ 67°.',
    'aurora_intensity_kR_typical': '오로라 일반 강도 (kR, 킬로레일리). 지구 ≈ 10.',
    'aurora_visibility_fraction_year': '연중 오로라 가시 비율 (0–1).',

    # ── Scatterer (atmosphere optics) ──────────────────────────────────────
    'sunset_color_hex':            '터미네이터 천정 방향 일몰 색 hex.',
    'mie_scattering_aerosol_anisotropy_g': 'Mie 산란 비대칭 인자 (-1..1). 지구 에어로졸 ≈ 0.76.',
}
