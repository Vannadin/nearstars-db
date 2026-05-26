# 원소별 플라즈마 색상

주기율표 원소별 불꽃 반응 / 저온 플라즈마 색상 사전. Helmenstine 2017 차트(sciencenotes.org)는 장식용 그라디언트 때문에 정확한 hex 가 안 보여서, 화학 문헌 + NIST 원자 스펙트럼 DB 를 1차 출처로 쓰고 차트는 시각 sanity check 로만 활용합니다.

정본 데이터: `db/refs/element_plasma_colors.yaml`. 이 문서는 `scripts/refs/render_element_colors_doc.py` 가 자동 생성합니다 — 직접 편집 금지.

## 상태(status) 범례

| 상태 | 의미 | Hex |
|---|---|---|
| 관측 가능 | 불꽃/플라즈마 색이 문헌에 기록됨 | 필수 |
| 불꽃색 없음 | 원소 자체는 존재하나 가시 불꽃색이 없음 | null |
| 가시광선 밖 | 방출선이 380–780 nm 밖에만 있음 | null |
| 방사능 위험 | 불꽃 반응 자체가 안전상 불가 | null |
| 반감기 부족 | 합성 원소, 관측 전 붕괴 | null |
| 자료 없음 | 문헌이 침묵 | null |

재진입 플라즈마(8,000–15,000 K)는 원자 불꽃 방출과 다릅니다 — 분자 밴드(N2+, C2 Swan, CN violet)가 우세합니다. Firefly cfg 의 bulk gas 색은 [composition-color reference](../../../.claude/skills/firefly-cfg/references/composition-color.md) 를 참고하세요.

## 1주기

| Z | Sym | Name | Color | Status | hex_basis | Basis |
|---|-----|------|-------|--------|-----------|-------|
| 1 | **H** | Hydrogen | <span style="display:inline-block;width:1em;height:1em;background:#ffaab9;border:1px solid #444;vertical-align:middle"></span> `#ffaab9` | 관측 가능 | cie_computed | Balmer Hα 656nm (red) dominant + Hβ 486nm (cyan); perceptual mix → hot pink |
| 2 | **He** | Helium | <span style="display:inline-block;width:1em;height:1em;background:#ffa07a;border:1px solid #444;vertical-align:middle"></span> `#ffa07a` | 관측 가능 | canonical_descriptor | He I D3 587.6nm + multiple visible lines; discharge tube appears peach-orange |

## 2주기

| Z | Sym | Name | Color | Status | hex_basis | Basis |
|---|-----|------|-------|--------|-----------|-------|
| 3 | **Li** | Lithium | <span style="display:inline-block;width:1em;height:1em;background:#dc143c;border:1px solid #444;vertical-align:middle"></span> `#dc143c` | 관측 가능 | canonical_descriptor | Li I doublet 670.8nm (resonance); classical crimson flame |
| 4 | **Be** | Beryllium | — | 불꽃색 없음 | — | BeO/BeF salts produce no visible flame coloration; toxicity prevents standard flame-test |
| 5 | **B** | Boron | <span style="display:inline-block;width:1em;height:1em;background:#3fcfa8;border:1px solid #444;vertical-align:middle"></span> `#3fcfa8` | 관측 가능 | canonical_descriptor | BO2 green bands 518/546nm dominant; classical bright green flame |
| 6 | **C** | Carbon | <span style="display:inline-block;width:1em;height:1em;background:#79ff2b;border:1px solid #444;vertical-align:middle"></span> `#79ff2b` | 관측 가능 | cie_computed | Hot graphite continuum (incandescence) + C2 Swan bands 516/473nm in cool plasma; chart renders amber/orange for soot luminescence |
| 7 | **N** | Nitrogen | <span style="display:inline-block;width:1em;height:1em;background:#ff0071;border:1px solid #444;vertical-align:middle"></span> `#ff0071` | 관측 가능 | cie_computed | Atomic N is faint blue-violet in low-temp plasma; flame chemistry typically dark |
| 8 | **O** | Oxygen | <span style="display:inline-block;width:1em;height:1em;background:#ffda00;border:1px solid #444;vertical-align:middle"></span> `#ffda00` | 관측 가능 | cie_computed | OI 777nm + 615nm + auroral 558/630nm lines; cool plasma appears pale blue |
| 9 | **F** | Fluorine | <span style="display:inline-block;width:1em;height:1em;background:#ff0000;border:1px solid #444;vertical-align:middle"></span> `#ff0000` | 관측 가능 | cie_computed | F I strongest lines are 685.6/690.2nm (deep red) and many in IR; perceptually faint, often categorized as no visible color |
| 10 | **Ne** | Neon | <span style="display:inline-block;width:1em;height:1em;background:#ff9300;border:1px solid #444;vertical-align:middle"></span> `#ff9300` | 관측 가능 | cie_computed | Ne I 640.2nm + cluster of red-orange lines; discharge tube orange-red signature |

## 3주기

| Z | Sym | Name | Color | Status | hex_basis | Basis |
|---|-----|------|-------|--------|-----------|-------|
| 11 | **Na** | Sodium | <span style="display:inline-block;width:1em;height:1em;background:#ffdf00;border:1px solid #444;vertical-align:middle"></span> `#ffdf00` | 관측 가능 | canonical_descriptor | Na D-line doublet 589.0/589.6nm; classical bright yellow flame |
| 12 | **Mg** | Magnesium | <span style="display:inline-block;width:1em;height:1em;background:#f5f5f5;border:1px solid #444;vertical-align:middle"></span> `#f5f5f5` | 관측 가능 | canonical_descriptor | Mg I 285.2nm (UV) + green bands; pyrotechnic flame is brilliant white from continuum |
| 13 | **Al** | Aluminum | <span style="display:inline-block;width:1em;height:1em;background:#e8e8e8;border:1px solid #444;vertical-align:middle"></span> `#e8e8e8` | 관측 가능 | canonical_descriptor | Al I 396.2/394.4nm UV-violet emission. Real Al combustion (aluminum-powder pyrotechnics, thermite) appears brilliant white from Al2O3 thermal incandescence — continuum rather than atomic emission. Canonical descriptor is 'brilliant white'. |
| 14 | **Si** | Silicon | — | 자료 없음 | — | No standard flame test; SiO2 vaporization color not characterized in normal flame conditions |
| 15 | **P** | Phosphorus | <span style="display:inline-block;width:1em;height:1em;background:#9fffae;border:1px solid #444;vertical-align:middle"></span> `#9fffae` | 관측 가능 | canonical_descriptor | P2 + HPO bands 525/540nm; pale green-white chemiluminescence |
| 16 | **S** | Sulfur | <span style="display:inline-block;width:1em;height:1em;background:#4fb0ff;border:1px solid #444;vertical-align:middle"></span> `#4fb0ff` | 관측 가능 | canonical_descriptor | SO2 + S2 bands 280–320nm UV; visible flame is pale blue |
| 17 | **Cl** | Chlorine | <span style="display:inline-block;width:1em;height:1em;background:#ff0000;border:1px solid #444;vertical-align:middle"></span> `#ff0000` | 관측 가능 | cie_computed | Cl2 discharge has bands in green-yellow + Cl I 754nm; flame chemistry adds CuCl2 → green |
| 18 | **Ar** | Argon | <span style="display:inline-block;width:1em;height:1em;background:#a06bff;border:1px solid #444;vertical-align:middle"></span> `#a06bff` | 관측 가능 | canonical_descriptor | Ar I multi-line in red + 696.5nm + UV; discharge tube classic violet-lilac |

## 4주기

| Z | Sym | Name | Color | Status | hex_basis | Basis |
|---|-----|------|-------|--------|-----------|-------|
| 19 | **K** | Potassium | <span style="display:inline-block;width:1em;height:1em;background:#c8a2c8;border:1px solid #444;vertical-align:middle"></span> `#c8a2c8` | 관측 가능 | canonical_descriptor | K I 766.5/769.9nm IR doublet + 404nm violet; flame appears lilac (pink-violet) |
| 20 | **Ca** | Calcium | <span style="display:inline-block;width:1em;height:1em;background:#ff6347;border:1px solid #444;vertical-align:middle"></span> `#ff6347` | 관측 가능 | canonical_descriptor | CaO bands 622/553nm + Ca I 422.7nm; classical orange-red ("brick red") flame |
| 21 | **Sc** | Scandium | — | 자료 없음 | — | No documented flame test color in standard references |
| 22 | **Ti** | Titanium | <span style="display:inline-block;width:1em;height:1em;background:#26ff2f;border:1px solid #444;vertical-align:middle"></span> `#26ff2f` | 관측 가능 | cie_computed | Ti I green cluster 498/506/519/520nm + Ti II 453nm blue. Atomic Ti emission in plasma/arc discharge is dominantly green from the visible Ti I lines. |
| 23 | **V** | Vanadium | <span style="display:inline-block;width:1em;height:1em;background:#e8e83b;border:1px solid #444;vertical-align:middle"></span> `#e8e83b` | 관측 가능 | chart_approx | V I + V II yellow-green band system; characteristic yellow-green flame from vanadium salts |
| 24 | **Cr** | Chromium | <span style="display:inline-block;width:1em;height:1em;background:#38ff02;border:1px solid #444;vertical-align:middle"></span> `#38ff02` | 관측 가능 | cie_computed | Cr I 520.4/520.6/520.8nm triplet — the famous 'chrome-green' responsible for emerald color in chromium-containing minerals (emerald, ruby, alexandrite). The chart's orange-yellow depiction does not match chromium's true atomic spectrum. |
| 25 | **Mn** | Manganese | <span style="display:inline-block;width:1em;height:1em;background:#9be88f;border:1px solid #444;vertical-align:middle"></span> `#9be88f` | 관측 가능 | canonical_descriptor | Mn I lines in green-yellow; characteristic yellow-green flame |
| 26 | **Fe** | Iron | <span style="display:inline-block;width:1em;height:1em;background:#f0a830;border:1px solid #444;vertical-align:middle"></span> `#f0a830` | 관측 가능 | canonical_descriptor | Fe I multi-line cluster 372/382nm UV + visible neutral Fe lines; flame and arc give gold-orange |
| 27 | **Co** | Cobalt | — | 자료 없음 | — | No characteristic visible flame color; Co salts mostly black/blue solids |
| 28 | **Ni** | Nickel | — | 자료 없음 | — | No characteristic visible flame color in standard chemistry references |
| 29 | **Cu** | Copper | <span style="display:inline-block;width:1em;height:1em;background:#3fe88f;border:1px solid #444;vertical-align:middle"></span> `#3fe88f` | 관측 가능 | canonical_descriptor | CuCl/CuBr bands 510/515nm; classical emerald-green flame (CuCl gives bluest, pure Cu greenest) |
| 30 | **Zn** | Zinc | <span style="display:inline-block;width:1em;height:1em;background:#00cdff;border:1px solid #444;vertical-align:middle"></span> `#00cdff` | 관측 가능 | cie_computed | Zn I 481.0nm + 472.2nm blue-green; flame appears cyan-bluish |
| 31 | **Ga** | Gallium | <span style="display:inline-block;width:1em;height:1em;background:#8500ff;border:1px solid #444;vertical-align:middle"></span> `#8500ff` | 관측 가능 | cie_computed | Ga I 403/417nm violet doublet; flame appears violet-blue |
| 32 | **Ge** | Germanium | — | 가시광선 밖 | — | Ge I dominant emission UV (265/270/304nm electronic). Visible lines 535/572nm perceptually negligible vs thermal continuum. No documented characteristic flame color. |
| 33 | **As** | Arsenic | — | 가시광선 밖 | — | As I dominant UV (235/278/286nm). Visible 615nm orange faint single line. Real arsenic flame appears pale-bluish white from oxide incandescence rather than atomic As emission. |
| 34 | **Se** | Selenium | <span style="display:inline-block;width:1em;height:1em;background:#00ffc8;border:1px solid #444;vertical-align:middle"></span> `#00ffc8` | 관측 가능 | cie_computed | Se I 473.1/479.9nm blue doublet + 506nm green minor. Selenium discharge is characteristically pale blue. |
| 35 | **Br** | Bromine | <span style="display:inline-block;width:1em;height:1em;background:#54ff3f;border:1px solid #444;vertical-align:middle"></span> `#54ff3f` | 관측 가능 | cie_computed | Br I red lines 470–600nm + Br2 vapor red-brown; flame red-orange |
| 36 | **Kr** | Krypton | <span style="display:inline-block;width:1em;height:1em;background:#e9ff00;border:1px solid #444;vertical-align:middle"></span> `#e9ff00` | 관측 가능 | cie_computed | Kr I 587.1/758.7nm + UV cluster; discharge appears whitish with pinkish tint |

## 5주기

| Z | Sym | Name | Color | Status | hex_basis | Basis |
|---|-----|------|-------|--------|-----------|-------|
| 37 | **Rb** | Rubidium | <span style="display:inline-block;width:1em;height:1em;background:#c30b4e;border:1px solid #444;vertical-align:middle"></span> `#c30b4e` | 관측 가능 | canonical_descriptor | Rb I 780/795nm IR + 420.2nm violet; flame is red-violet |
| 38 | **Sr** | Strontium | <span style="display:inline-block;width:1em;height:1em;background:#dc143c;border:1px solid #444;vertical-align:middle"></span> `#dc143c` | 관측 가능 | canonical_descriptor | SrCl band 605/640nm + Sr I 460.7nm; classical crimson red flame, brightest emitter |
| 39 | **Y** | Yttrium | <span style="display:inline-block;width:1em;height:1em;background:#ff6601;border:1px solid #444;vertical-align:middle"></span> `#ff6601` | 관측 가능 | cie_computed | YO molecular band system 615-648nm orange-red dominates yttrium flame chemistry (YCl3, YNO3 salts). Atomic Y I 410nm violet is weaker. The chart's yellow depiction leans toward green-yellow rather than the spectroscopic orange-red. |
| 40 | **Zr** | Zirconium | <span style="display:inline-block;width:1em;height:1em;background:#5fa3e8;border:1px solid #444;vertical-align:middle"></span> `#5fa3e8` | 관측 가능 | chart_approx | ZrO bands in blue; metal combustion produces brilliant white-blue |
| 41 | **Nb** | Niobium | <span style="display:inline-block;width:1em;height:1em;background:#5fa3e8;border:1px solid #444;vertical-align:middle"></span> `#5fa3e8` | 관측 가능 | chart_approx | Nb I + NbO band system in blue; spectroscopically blue-violet |
| 42 | **Mo** | Molybdenum | <span style="display:inline-block;width:1em;height:1em;background:#99ff00;border:1px solid #444;vertical-align:middle"></span> `#99ff00` | 관측 가능 | cie_computed | Mo I 550-553nm yellow-green doublet. Documented in molybdenum arc discharges and molybdate flame chemistry. |
| 43 | **Tc** | Technetium | — | 방사능 위험 | — | All Tc isotopes radioactive; standard flame test unsafe |
| 44 | **Ru** | Ruthenium | — | 자료 없음 | — | No characteristic visible flame color documented |
| 45 | **Rh** | Rhodium | — | 자료 없음 | — | No documented flame color |
| 46 | **Pd** | Palladium | — | 자료 없음 | — | No documented flame color |
| 47 | **Ag** | Silver | — | 자료 없음 | — | No characteristic visible flame color |
| 48 | **Cd** | Cadmium | <span style="display:inline-block;width:1em;height:1em;background:#dc143c;border:1px solid #444;vertical-align:middle"></span> `#dc143c` | 관측 가능 | canonical_descriptor | Cd I 467.8/479.99nm green-blue but salts give brick-red flame |
| 49 | **In** | Indium | <span style="display:inline-block;width:1em;height:1em;background:#094bff;border:1px solid #444;vertical-align:middle"></span> `#094bff` | 관측 가능 | cie_computed | In I 410.2nm + 451.1nm blue-violet; flame indigo-blue (name origin) |
| 50 | **Sn** | Tin | — | 가시광선 밖 | — | Sn I dominant UV (235/284nm). Visible 452/563nm minor lines; tin flame appearance is pale blue-white incandescence from SnO/SnO2 rather than characteristic atomic emission. |
| 51 | **Sb** | Antimony | — | 가시광선 밖 | — | Sb I dominant UV (252/259nm). Visible 614/777nm faint. Antimony flame test appearance is pale blue-green from oxide incandescence rather than atomic Sb emission. |
| 52 | **Te** | Tellurium | <span style="display:inline-block;width:1em;height:1em;background:#8bff00;border:1px solid #444;vertical-align:middle"></span> `#8bff00` | 관측 가능 | cie_computed | Te I 525-567nm green band. Tellurium halide flame chemistry gives characteristic pale green. |
| 53 | **I** | Iodine | <span style="display:inline-block;width:1em;height:1em;background:#95ff00;border:1px solid #444;vertical-align:middle"></span> `#95ff00` | 관측 가능 | cie_computed | I I 511.0nm + 533.8nm + 546.5nm green-blue; I2 sublimation violet vapor |
| 54 | **Xe** | Xenon | <span style="display:inline-block;width:1em;height:1em;background:#0094ff;border:1px solid #444;vertical-align:middle"></span> `#0094ff` | 관측 가능 | cie_computed | Xe I multi-line; discharge tube blue-violet, xenon arc resembles sunlight |

## 6주기 (주족 + 전이금속)

| Z | Sym | Name | Color | Status | hex_basis | Basis |
|---|-----|------|-------|--------|-----------|-------|
| 55 | **Cs** | Cesium | <span style="display:inline-block;width:1em;height:1em;background:#3a4cd6;border:1px solid #444;vertical-align:middle"></span> `#3a4cd6` | 관측 가능 | canonical_descriptor | Cs I 852.1/894.3nm IR + 455.5nm blue; flame blue-violet |
| 56 | **Ba** | Barium | <span style="display:inline-block;width:1em;height:1em;background:#7fe83b;border:1px solid #444;vertical-align:middle"></span> `#7fe83b` | 관측 가능 | canonical_descriptor | BaO + BaCl bands 524nm + Ba I 553.5nm; classical pale apple-green flame |
| 72 | **Hf** | Hafnium | <span style="display:inline-block;width:1em;height:1em;background:#c8e8e8;border:1px solid #444;vertical-align:middle"></span> `#c8e8e8` | 관측 가능 | chart_approx | Hf I lines spread across visible; appearance pale gray-cyan |
| 73 | **Ta** | Tantalum | <span style="display:inline-block;width:1em;height:1em;background:#3b9be8;border:1px solid #444;vertical-align:middle"></span> `#3b9be8` | 관측 가능 | chart_approx | Ta I + TaO bands in blue; chart renders blue |
| 74 | **W** | Tungsten | <span style="display:inline-block;width:1em;height:1em;background:#8bff00;border:1px solid #444;vertical-align:middle"></span> `#8bff00` | 관측 가능 | cie_computed | W I 540/547nm green cluster + 522/560 secondary. Documented in tungsten lamp discharge spectra. |
| 75 | **Re** | Rhenium | <span style="display:inline-block;width:1em;height:1em;background:#6cff3d;border:1px solid #444;vertical-align:middle"></span> `#6cff3d` | 관측 가능 | cie_computed | Re I 488-528nm green cluster + 581nm yellow. Atomic rhenium plasma emission falls in cyan-green to yellow. |
| 76 | **Os** | Osmium | — | 자료 없음 | — | No characteristic visible flame color documented |
| 77 | **Ir** | Iridium | — | 자료 없음 | — | No documented flame color |
| 78 | **Pt** | Platinum | — | 자료 없음 | — | No characteristic visible flame color (Pt is the standard reference wire for flame tests precisely because it's inert) |
| 79 | **Au** | Gold | — | 자료 없음 | — | No documented flame color |
| 80 | **Hg** | Mercury | <span style="display:inline-block;width:1em;height:1em;background:#c8ff04;border:1px solid #444;vertical-align:middle"></span> `#c8ff04` | 관측 가능 | cie_computed | Hg I 546.1nm green + 435.8nm blue + 404.7nm violet; discharge tube green-tinted |
| 81 | **Tl** | Thallium | <span style="display:inline-block;width:1em;height:1em;background:#3fe83f;border:1px solid #444;vertical-align:middle"></span> `#3fe83f` | 관측 가능 | canonical_descriptor | Tl I 535.0nm green singlet; classical bright green flame |
| 82 | **Pb** | Lead | <span style="display:inline-block;width:1em;height:1em;background:#bf00ff;border:1px solid #444;vertical-align:middle"></span> `#bf00ff` | 관측 가능 | cie_computed | Pb I 405.8nm violet + 368.3nm UV; flame pale blue or grayish |
| 83 | **Bi** | Bismuth | <span style="display:inline-block;width:1em;height:1em;background:#05b0ff;border:1px solid #444;vertical-align:middle"></span> `#05b0ff` | 관측 가능 | cie_computed | Bi I 472.3nm + 422.8nm; flame pale blue-cyan |
| 84 | **Po** | Polonium | — | 방사능 위험 | — | All Po isotopes radioactive; flame test unsafe |
| 85 | **At** | Astatine | — | 방사능 위험 | — | All At isotopes radioactive with t½ ≤ 8 hours; no flame test data |
| 86 | **Rn** | Radon | — | 방사능 위험 | — | Radioactive noble gas; discharge in trace amounts only, not characterized for flame test |

## 란타넘족

| Z | Sym | Name | Color | Status | hex_basis | Basis |
|---|-----|------|-------|--------|-----------|-------|
| 57 | **La** | Lanthanum | — | 자료 없음 | — | No documented visible flame color |
| 58 | **Ce** | Cerium | <span style="display:inline-block;width:1em;height:1em;background:#5fa3e8;border:1px solid #444;vertical-align:middle"></span> `#5fa3e8` | 관측 가능 | chart_approx | Ce-glass discharge yields blue; CeO2 incandesces pale yellow-white |
| 59 | **Pr** | Praseodymium | <span style="display:inline-block;width:1em;height:1em;background:#e83fc8;border:1px solid #444;vertical-align:middle"></span> `#e83fc8` | 관측 가능 | chart_approx | Pr3+ in solid yields green; in flame emission complex multi-line; chart renders magenta |
| 60 | **Nd** | Neodymium | <span style="display:inline-block;width:1em;height:1em;background:#c83be8;border:1px solid #444;vertical-align:middle"></span> `#c83be8` | 관측 가능 | chart_approx | Nd3+ multi-line absorption + emission across visible; chart renders violet |
| 61 | **Pm** | Promethium | — | 방사능 위험 | — | All Pm isotopes radioactive (longest t½ 17.7 yr); standard flame test not performed |
| 62 | **Sm** | Samarium | <span style="display:inline-block;width:1em;height:1em;background:#e8c5a8;border:1px solid #444;vertical-align:middle"></span> `#e8c5a8` | 관측 가능 | chart_approx | Sm I multi-line + Sm3+ band emission; chart renders pale peach |
| 63 | **Eu** | Europium | <span style="display:inline-block;width:1em;height:1em;background:#b87fd6;border:1px solid #444;vertical-align:middle"></span> `#b87fd6` | 관측 가능 | chart_approx | Eu I + Eu3+ red phosphor 612nm; chart renders pale violet |
| 64 | **Gd** | Gadolinium | <span style="display:inline-block;width:1em;height:1em;background:#e8a83b;border:1px solid #444;vertical-align:middle"></span> `#e8a83b` | 관측 가능 | chart_approx | Gd I multi-line; chart renders orange |
| 65 | **Tb** | Terbium | <span style="display:inline-block;width:1em;height:1em;background:#e8d83b;border:1px solid #444;vertical-align:middle"></span> `#e8d83b` | 관측 가능 | chart_approx | Tb3+ green phosphor 545nm; chart renders yellow-green |
| 66 | **Dy** | Dysprosium | <span style="display:inline-block;width:1em;height:1em;background:#7fe8c8;border:1px solid #444;vertical-align:middle"></span> `#7fe8c8` | 관측 가능 | chart_approx | Dy I multi-line; chart renders pale cyan-green |
| 67 | **Ho** | Holmium | <span style="display:inline-block;width:1em;height:1em;background:#3fe83b;border:1px solid #444;vertical-align:middle"></span> `#3fe83b` | 관측 가능 | chart_approx | Ho3+ visible band emission; chart renders bright green |
| 68 | **Er** | Erbium | <span style="display:inline-block;width:1em;height:1em;background:#3fe85f;border:1px solid #444;vertical-align:middle"></span> `#3fe85f` | 관측 가능 | chart_approx | Er3+ multi-line + green band; chart renders pale green |
| 69 | **Tm** | Thulium | <span style="display:inline-block;width:1em;height:1em;background:#7fe8af;border:1px solid #444;vertical-align:middle"></span> `#7fe8af` | 관측 가능 | chart_approx | Tm3+ blue band emission; chart renders pale cyan |
| 70 | **Yb** | Ytterbium | <span style="display:inline-block;width:1em;height:1em;background:#5fe8c8;border:1px solid #444;vertical-align:middle"></span> `#5fe8c8` | 관측 가능 | chart_approx | Yb3+ visible band emission; chart renders pale teal |
| 71 | **Lu** | Lutetium | <span style="display:inline-block;width:1em;height:1em;background:#5fe8e8;border:1px solid #444;vertical-align:middle"></span> `#5fe8e8` | 관측 가능 | chart_approx | Lu I multi-line; chart renders pale cyan |

## 7주기 (주족 + 전이금속)

| Z | Sym | Name | Color | Status | hex_basis | Basis |
|---|-----|------|-------|--------|-----------|-------|
| 87 | **Fr** | Francium | — | 방사능 위험 | — | Longest-lived isotope t½ ≈ 22 minutes; predicted similar to Cs but never observed |
| 88 | **Ra** | Radium | <span style="display:inline-block;width:1em;height:1em;background:#dc143c;border:1px solid #444;vertical-align:middle"></span> `#dc143c` | 관측 가능 | canonical_descriptor | Predicted/observed crimson flame in line with alkaline-earth pattern (Sr-like); radium salts genuinely emit red |
| 104 | **Rf** | Rutherfordium | — | 반감기 부족 | — | Half-life of seconds to minutes; no flame test possible |
| 105 | **Db** | Dubnium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 106 | **Sg** | Seaborgium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 107 | **Bh** | Bohrium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 108 | **Hs** | Hassium | — | 반감기 부족 | — | Half-life ≤ 10 seconds; no observation |
| 109 | **Mt** | Meitnerium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 110 | **Ds** | Darmstadtium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 111 | **Rg** | Roentgenium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 112 | **Cn** | Copernicium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 113 | **Nh** | Nihonium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 114 | **Fl** | Flerovium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 115 | **Mc** | Moscovium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 116 | **Lv** | Livermorium | — | 반감기 부족 | — | Half-life seconds; no observation |
| 117 | **Ts** | Tennessine | — | 반감기 부족 | — | Half-life seconds; no observation |
| 118 | **Og** | Oganesson | — | 반감기 부족 | — | Half-life milliseconds; no observation |

## 악티늄족

| Z | Sym | Name | Color | Status | hex_basis | Basis |
|---|-----|------|-------|--------|-----------|-------|
| 89 | **Ac** | Actinium | — | 방사능 위험 | — | Radioactive (t½ 21.8 yr for 227Ac); no documented flame test |
| 90 | **Th** | Thorium | <span style="display:inline-block;width:1em;height:1em;background:#e8e8e8;border:1px solid #444;vertical-align:middle"></span> `#e8e8e8` | 관측 가능 | canonical_descriptor | ThO2-impregnated Welsbach gas mantle: brilliant white thermal continuum + selective IR emission. Discovered 1885 (Auer von Welsbach), commercialized in gas lamps. Canonical 'brilliant white' descriptor. |
| 91 | **Pa** | Protactinium | — | 방사능 위험 | — | All Pa isotopes radioactive; no flame test characterized |
| 92 | **U** | Uranium | <span style="display:inline-block;width:1em;height:1em;background:#cfe83b;border:1px solid #444;vertical-align:middle"></span> `#cfe83b` | 관측 가능 | canonical_descriptor | Uranium signature green from two combined mechanisms: (a) UO2 thermal incandescence in oxidizing flame and (b) U(VI) fluorescence (uranyl ion ~520nm emission) in uranium glass under UV. Both produce the same yellow-green descriptor. |
| 93 | **Np** | Neptunium | — | 방사능 위험 | — | All Np isotopes radioactive; standard flame test not performed |
| 94 | **Pu** | Plutonium | — | 방사능 위험 | — | Highly radioactive; flame test unsafe |
| 95 | **Am** | Americium | — | 방사능 위험 | — | Radioactive; flame test unsafe |
| 96 | **Cm** | Curium | — | 방사능 위험 | — | Radioactive; flame test unsafe |
| 97 | **Bk** | Berkelium | — | 방사능 위험 | — | Radioactive; no characterized flame test |
| 98 | **Cf** | Californium | — | 방사능 위험 | — | Radioactive; no characterized flame test |
| 99 | **Es** | Einsteinium | — | 방사능 위험 | — | Radioactive; quantities insufficient for flame test |
| 100 | **Fm** | Fermium | — | 방사능 위험 | — | Radioactive; only synthesized in trace amounts |
| 101 | **Md** | Mendelevium | — | 반감기 부족 | — | Longest-lived isotope t½ ≈ 51.5 days; insufficient for flame test |
| 102 | **False** | Nobelium | — | 반감기 부족 | — | Longest-lived isotope t½ ≈ 58 minutes |
| 103 | **Lr** | Lawrencium | — | 반감기 부족 | — | Longest-lived isotope t½ ≈ 11 hours |

## Related

- [composition-color (firefly-cfg 스킬)](../../../.claude/skills/firefly-cfg/references/composition-color.md) — 재진입 plasma bulk gas 팔레트 (다른 물리 영역)
- [phase3-mapping (firefly-cfg 스킬)](../../../.claude/skills/firefly-cfg/references/phase3-mapping.md) — Phase 3 → Firefly 필드 매핑
