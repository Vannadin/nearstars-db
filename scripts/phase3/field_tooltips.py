# Phase 3 Decisions 표 필드명 호버 툴팁 사전 (한/영 양언어)
"""Bilingual tooltip text for standard cfg field names that appear in
Decisions tables and prose. Loaded by build_html.py to wrap
`<code>...</code>` blocks whose content matches a known field with a
`.field-tt` span carrying both `data-ko-tip` and `data-en-tip`.

Tooltip language follows the page lang toggle. Field names themselves
stay in English/code regardless of language.
"""

FIELD_TOOLTIPS: dict[str, dict[str, str]] = {
    # ── Orbital ────────────────────────────────────────────────────────────
    'tidally_locked': {
        'ko': '조석 고정 여부. 행성이 모항성에 한 면만 보임 (true/false).',
        'en': 'Tidal locking — same hemisphere always faces the host star (true/false).',
    },
    'obliquity_deg': {
        'ko': '자전축 기울기 (도). 지구 ≈ 23.5°.',
        'en': 'Axial tilt in degrees. Earth ≈ 23.5°.',
    },
    'eccentricity': {
        'ko': '궤도 이심률. 0 = 정원, 1 = 포물선.',
        'en': 'Orbital eccentricity. 0 = circle, 1 = parabolic.',
    },
    'argument_of_periastron_deg': {
        'ko': '근일점 인수 (도). 궤도면 위 근일점 방향.',
        'en': 'Argument of periastron (degrees). Direction of closest approach within the orbit plane.',
    },
    'sidereal_period_days': {
        'ko': '항성일 기준 자전 주기 (일).',
        'en': 'Sidereal rotation period (days).',
    },
    'semi_major_axis_au': {
        'ko': '궤도 긴반지름 (AU, 1 AU = 지구–태양 거리).',
        'en': 'Orbital semi-major axis in AU (1 AU = Earth–Sun distance).',
    },
    'inclination_deg': {
        'ko': '시선 방향에 대한 궤도면 기울기 (도).',
        'en': 'Orbital inclination relative to line of sight (degrees).',
    },

    # ── Physical ───────────────────────────────────────────────────────────
    'mass_mearth': {
        'ko': '질량 (지구질량 단위).',
        'en': 'Mass in Earth-mass units.',
    },
    'radius_rearth': {
        'ko': '반지름 (지구반지름 단위).',
        'en': 'Radius in Earth-radius units.',
    },
    'surface_gravity_g_earth': {
        'ko': '표면 중력 (지구 중력 1.0 단위).',
        'en': 'Surface gravity in Earth-g units.',
    },
    'density_g_cc': {
        'ko': '평균 밀도 (g/cm³). 지구 ≈ 5.5.',
        'en': 'Bulk density in g/cm³. Earth ≈ 5.5.',
    },
    'insolation_s_earth': {
        'ko': '항성으로부터 받는 복사 (지구 일조량 단위).',
        'en': 'Stellar irradiance at the planet, in Earth-insolation units.',
    },
    'equilibrium_temp_k': {
        'ko': '평형 온도 (K). 대기·온실효과 없이 흡수-방사 균형 가정.',
        'en': 'Equilibrium temperature (K) assuming no atmosphere and pure radiative balance.',
    },
    'bond_albedo': {
        'ko': '본드 반사율. 전 파장 통합 반사율 (0–1).',
        'en': 'Bond albedo. Fraction of stellar power reflected, integrated over all wavelengths (0–1).',
    },
    'water_mass_fraction': {
        'ko': '물 질량 분율. 지구 ≈ 0.0002.',
        'en': 'Water mass fraction of the planet. Earth ≈ 0.0002.',
    },

    # ── Atmosphere ─────────────────────────────────────────────────────────
    'atmosphere_present': {
        'ko': '대기 존재 여부 (true/false 또는 정성 표현).',
        'en': 'Whether the planet has an atmosphere (true/false or qualitative).',
    },
    'atmosphere_surface_pressure_pa': {
        'ko': '표면 대기압 (Pa). 1 bar = 100,000 Pa.',
        'en': 'Surface atmospheric pressure in Pa. 1 bar = 100,000 Pa.',
    },
    'atmosphere_composition': {
        'ko': '대기 조성 (주 성분과 분압 비율).',
        'en': 'Atmospheric composition — main species and partial pressures.',
    },
    'atmosphere_scale_height_km': {
        'ko': '대기 스케일 높이 (km). 압력이 1/e 로 떨어지는 고도.',
        'en': 'Atmospheric scale height in km — altitude at which pressure drops by 1/e.',
    },
    'atmosphere_tint_rgb_hex': {
        'ko': '대기 limb (가장자리) 색조 hex.',
        'en': 'Atmospheric limb tint as a hex color.',
    },
    'cloud_cover_fraction': {
        'ko': '구름 피복률 (0–1).',
        'en': 'Cloud cover fraction (0–1).',
    },
    'cloud_morphology': {
        'ko': '구름 형태 (위도/경도 패턴 서술).',
        'en': 'Cloud morphology — latitude/longitude patterns.',
    },
    'cloud_tint_rgb_hex': {
        'ko': '구름 색조 hex.',
        'en': 'Cloud tint as a hex color.',
    },

    # ── Surface ────────────────────────────────────────────────────────────
    'dayside_surface_temp_k': {
        'ko': '주간면 표면 온도 (K).',
        'en': 'Dayside surface temperature (K).',
    },
    'nightside_surface_temp_k': {
        'ko': '야간면 표면 온도 (K).',
        'en': 'Nightside surface temperature (K).',
    },
    'surface_temp_substellar_k': {
        'ko': 'substellar (모항성 직하점) 표면 온도 (K).',
        'en': 'Substellar (sub-host-star) surface temperature (K).',
    },
    'surface_temp_nightside_k': {
        'ko': '야간면 표면 온도 (K).',
        'en': 'Nightside surface temperature (K).',
    },
    'surface_temp_global_mean_k': {
        'ko': '전구 평균 표면 온도 (K).',
        'en': 'Global mean surface temperature (K).',
    },
    'dayside_brightness_temp_k': {
        'ko': 'JWST 등에서 측정한 주간면 밝기 온도 (K, 파장대별).',
        'en': 'Dayside brightness temperature (K) measured per JWST filter band.',
    },
    'surface_tint_rgb_hex_primary': {
        'ko': '표면 주 색조 hex.',
        'en': 'Primary surface tint as a hex color.',
    },
    'surface_tint_rgb_hex_accent': {
        'ko': '표면 보조 색조 hex (스팟·패치).',
        'en': 'Accent surface tint as a hex color (spots / patches).',
    },
    'surface_morphology': {
        'ko': '표면 지형 서술 (크레이터·용암류·빙하 등).',
        'en': 'Surface morphology — craters, lava flows, glaciers, etc.',
    },
    'surface_ice_caps': {
        'ko': '극관·전구 빙상 분포.',
        'en': 'Ice cap / global ice sheet distribution.',
    },
    'ocean_present': {
        'ko': '표면 액체수 해양 존재 여부.',
        'en': 'Whether liquid-water surface ocean is present.',
    },
    'ocean_extent_substellar_radius_deg': {
        'ko': 'substellar 지점 중심 열대 호수 반경 (도).',
        'en': 'Substellar open-water disk radius in degrees of arc.',
    },
    'ocean_tint_rgb_hex': {
        'ko': '해양 색조 hex.',
        'en': 'Ocean tint as a hex color.',
    },

    # ── Interior heating ───────────────────────────────────────────────────
    'tidal_heating_w_m2': {
        'ko': '조석 가열 표면 flux (W/m²). Io ≈ 2.',
        'en': 'Tidal heating surface flux (W/m²). Io ≈ 2.',
    },
    'induction_heating_w_m2': {
        'ko': '항성 자기장 유도 가열 (W/m²).',
        'en': 'Stellar-field induction heating (W/m²).',
    },
    'radiogenic_heat_w_m2': {
        'ko': '방사성 동위원소 붕괴 열 (W/m²). 지구 ≈ 0.087.',
        'en': 'Radiogenic heat from isotope decay (W/m²). Earth ≈ 0.087.',
    },

    # ── Stellar / sky ──────────────────────────────────────────────────────
    'star_apparent_angular_diameter_deg': {
        'ko': '하늘에서 모항성의 시직경 (도). 지구에서 본 태양 ≈ 0.53°.',
        'en': 'Host star angular diameter as seen from the planet (degrees). Sun-from-Earth ≈ 0.53°.',
    },
    'stellar_illumination_color_temp_k': {
        'ko': '모항성 색온도 (K). 태양 ≈ 5778, M dwarf ≈ 2500-3500.',
        'en': 'Host star illumination color temperature (K). Sun ≈ 5778, M dwarfs ≈ 2500–3500.',
    },
    'xuv_flux_at_planet_F_earth': {
        'ko': '행성에 도달하는 XUV flux (지구 단위).',
        'en': 'XUV flux at the planet, in Earth-flux units.',
    },
    'stellar_microflare_cadence_min': {
        'ko': '미세 플레어 평균 발생 간격 (분).',
        'en': 'Mean cadence between stellar microflares (minutes).',
    },

    # ── Kerbalism (radiation / magnetosphere) ──────────────────────────────
    'magnetic_field_present': {
        'ko': '전구 자기장 (다이나모) 존재 여부.',
        'en': 'Global magnetic dynamo present (true/false).',
    },
    'magnetic_field_strength_microtesla_equator': {
        'ko': '적도 자기장 강도 (μT). 지구 ≈ 30.',
        'en': 'Equatorial magnetic field strength (μT). Earth ≈ 30.',
    },
    'magnetic_dipole_moment_normalized_earth': {
        'ko': '쌍극자 모멘트 (지구 = 1.0 단위).',
        'en': 'Magnetic dipole moment in Earth units (Earth = 1.0).',
    },
    'magnetic_dipole_tilt_deg': {
        'ko': '자전축에 대한 쌍극자 기울기 (도). 지구 ≈ 11°.',
        'en': 'Dipole tilt relative to spin axis (degrees). Earth ≈ 11°.',
    },
    'magnetosphere_standoff_planet_radii': {
        'ko': '자기권 standoff 거리 (행성반지름 단위).',
        'en': 'Magnetopause standoff distance in planet radii.',
    },
    'radiation_belt_present': {
        'ko': '밴 앨런 형 방사선대 존재 여부.',
        'en': 'Van Allen-type trapped radiation belts present (true/false).',
    },
    'radiation_inner_belt_radius_planet_radii': {
        'ko': '내부 방사선대 반경 (행성반지름 단위).',
        'en': 'Inner radiation belt radius in planet radii.',
    },
    'radiation_outer_belt_radius_planet_radii': {
        'ko': '외부 방사선대 반경 (행성반지름 단위).',
        'en': 'Outer radiation belt radius in planet radii.',
    },
    'surface_radiation_dose_msv_yr': {
        'ko': '표면 연간 방사선량 (mSv/yr). 지구 ≈ 2.4.',
        'en': 'Annual surface radiation dose (mSv/yr). Earth natural ≈ 2.4.',
    },
    'atmospheric_shielding_g_cm2': {
        'ko': '대기 차폐량 (g/cm²). 지구 ≈ 1030.',
        'en': 'Atmospheric shielding column (g/cm²). Earth ≈ 1030.',
    },

    # ── EVE (aurora) ───────────────────────────────────────────────────────
    'aurora_present': {
        'ko': '오로라 발생 여부 (대기 + 자기장 동시 필요).',
        'en': 'Auroral activity present — requires both atmosphere and magnetic field.',
    },
    'aurora_color_primary_hex': {
        'ko': '주 오로라 색 hex. 발광 종(species) 에 의해 결정.',
        'en': 'Primary auroral color hex — determined by the dominant emission species.',
    },
    'aurora_color_secondary_hex': {
        'ko': '보조 오로라 색 hex.',
        'en': 'Secondary auroral color hex.',
    },
    'aurora_emission_species_primary': {
        'ko': '주 발광 종 (e.g. [OI] 557 nm, CO₂⁺ FDB).',
        'en': 'Primary auroral emission species (e.g. [OI] 557 nm, CO₂⁺ FDB).',
    },
    'aurora_oval_magnetic_latitude_deg': {
        'ko': '오로라 오벌 중심 자기 위도 (도). 지구 ≈ 67°.',
        'en': 'Auroral oval magnetic latitude (degrees). Earth ≈ 67°.',
    },
    'aurora_intensity_kR_typical': {
        'ko': '오로라 일반 강도 (kR, 킬로레일리). 지구 ≈ 10.',
        'en': 'Typical auroral intensity in kilorayleighs (kR). Earth ≈ 10.',
    },
    'aurora_visibility_fraction_year': {
        'ko': '연중 오로라 가시 비율 (0–1).',
        'en': 'Fraction of the year when auroras are visible (0–1).',
    },

    # ── Scatterer (atmosphere optics) ──────────────────────────────────────
    'sunset_color_hex': {
        'ko': '터미네이터 천정 방향 일몰 색 hex.',
        'en': 'Sunset color at the terminator zenith, as a hex color.',
    },
    'mie_scattering_aerosol_anisotropy_g': {
        'ko': 'Mie 산란 비대칭 인자 (-1..1). 지구 에어로졸 ≈ 0.76.',
        'en': 'Mie scattering asymmetry parameter g (-1..1). Earth aerosol ≈ 0.76.',
    },
}

# Backwards-compatible alias for the previous ko-only API.
FIELD_TOOLTIPS_KO: dict[str, str] = {k: v['ko'] for k, v in FIELD_TOOLTIPS.items()}
