# D2-nan 시험 — D2 줄 모듈(melt_exact · thermal_ale · hop_track)의 NaN 규칙: 자리마다 심은 NaN 은 이름 붙은 거절·None·0.0, 유한 쌍둥이는 고정값 그대로
"""Checks for D2-nan (artifacts d2nan-pkg-c8, pc/d2-nan-c8/plan.md rev 1 e1234269, cleared by 68 as 377a5faf).

N1–N9: each site gets a planted NaN, which must give the named refusal, None or 0.0 and never a sign, and a finite
twin, which must equal the value frozen at engine/stageA-d2 0c05bb5a (the fix leaves finite arithmetic as it was).
The already-guarded sites of plan §1 get one planted line each, so their guards stay pinned. The negative control
runs this file against 0c05bb5a's modules: every N line must be red there, every guarded line and twin green.

    python3 engine/test_d2_nan.py            (the checks)
    python3 engine/test_d2_nan.py --pins     (prints the finite twins' values, to freeze at 0c05bb5a)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fold_track as ft                # noqa: E402
import hop_track as hp                 # noqa: E402
import melt_exact                      # noqa: E402
import samuel_layer as lay             # noqa: E402
import samuel_model as sm              # noqa: E402
import samuel_structure as ss          # noqa: E402
import samuel_thermal as st            # noqa: E402
import thermal_ale as ta               # noqa: E402
import thermal_stack as ts             # noqa: E402

NAN = float("nan")
PINS_MODE = "--pins" in sys.argv
fails = 0
pins_out: dict = {}

#: The finite twins' values at engine/stageA-d2 0c05bb5a (python3 engine/test_d2_nan.py --pins there), as repr.
PINS = {
    'N1-N3 melt_integrals':
        "{'shallow_phi_v': 5.5970375363927155e+17, 'shallow_v': 9.549035042587947e+18, 'deep_phi_v': 0.0, 'deep_v': 0.0}",
    'N4 _radius_at':
        '2700000.0',
    'N5 event_signs':
        '(True, False, False, False, False, True, False, False, False, False, True, False, False, False, False, True)',
    'N6 hump_sign':
        '1.0',
    'N7 lid_coeffs':
        '(500.0, [0.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3997000.0, 3448500.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 2900000.0, 0.0], [0.0, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 1e-08, 3e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 0.0], [0.0, 1.599758317284435e-05, 1.599758353785506e-05, 1.599758390275553e-05, 1.5997584267545813e-05, 1.5997584632225955e-05, 1.5997584996796013e-05, 1.599758536125603e-05, 1.5997585725606065e-05, 1.5997586089846153e-05, 1.5997586453976357e-05, 1.5997586817996718e-05, 1.5997587181907297e-05, 1.5997587545708127e-05, 1.5997587909399274e-05, 1.5997588272980777e-05, 1.599758863645269e-05, 1.5997588999815063e-05, 1.5997589363067944e-05, 1.599758972621138e-05, 1.5997590089245428e-05, 1.5997590452170128e-05, 1.5997590814985534e-05, 1.5997591177691696e-05, 1.5997591540288666e-05, 1.5997591902776483e-05, 1.599759226515521e-05, 1.5997592627424886e-05, 1.5997592989585566e-05, 1.5997593351637293e-05, 1.5997593713580123e-05, 1.59975940754141e-05, 1.599759443713928e-05, 1.59975947987557e-05, 1.599759516026342e-05, 1.5997595521662483e-05, 1.5997595882952945e-05, 1.5997596244134848e-05, 1.5997596605208242e-05, 1.5997596966173176e-05, 1.5997597327029706e-05, 1.5997597687777867e-05, 1.5997598048417723e-05, 1.5997598408949308e-05, 1.5997598769372683e-05, 1.599759912968789e-05, 1.599759948989498e-05, 1.5997599849994e-05, 1.5997600209985e-05, 1.599760056986803e-05, 1.5997600929643136e-05, 1.5997601289310368e-05, 1.5997601648869776e-05, 1.59976020083214e-05, 1.59976023676653e-05, 1.5997602726901517e-05, 1.5997603086030103e-05, 1.5997603445051106e-05, 1.5997603803964573e-05, 1.599760416277055e-05, 1.599760452146909e-05, 1.5997604880060237e-05, 1.5997605238544046e-05, 1.5997605596920558e-05, 1.5997605955189826e-05, 1.599760631335189e-05, 1.5997606671406812e-05, 1.5997607029354625e-05, 1.599760738719539e-05, 1.5997607744929146e-05, 1.5997608102555947e-05, 1.5997608460075835e-05, 1.599760881748886e-05, 1.5997609174795073e-05, 1.599760953199452e-05, 1.5997609889087247e-05, 1.5997610246073308e-05, 1.599761060295274e-05, 1.5997610959725604e-05, 1.5997611316391936e-05, 1.599761167295179e-05, 1.5997612029405213e-05, 1.5997612385752252e-05, 1.599761274199295e-05, 1.5997613098127367e-05, 1.5997613454155535e-05, 1.5997613810077513e-05, 1.5997614165893343e-05, 1.5997614521603078e-05, 1.5997614877206757e-05, 1.5997615232704435e-05, 1.5997615588096153e-05, 1.5997615943381964e-05, 1.5997616298561914e-05, 1.5997616653636048e-05, 1.5997617008604412e-05, 1.5997617363467063e-05, 1.5997617718224034e-05, 1.5997618072875384e-05, 1.5997618427421153e-05, 1.5997618781861392e-05, 1.5997619136196145e-05, 1.5997619490425462e-05, 1.599761984454939e-05, 1.5997620198567974e-05, 1.599762055248126e-05, 1.59976209062893e-05, 1.5997621259992137e-05, 1.5997621613589818e-05, 1.599762196708239e-05, 1.5997622320469902e-05, 1.59976226737524e-05, 1.599762302692993e-05, 1.5997623380002535e-05, 1.599762373297027e-05, 1.5997624085833175e-05, 1.5997624438591302e-05, 1.599762479124469e-05, 1.5997625143793393e-05, 1.5997625496237453e-05, 1.5997625848576925e-05, 9.998516375507401e-06, 9.998516595588913e-06, 9.99851681560514e-06, 9.998517035556111e-06, 9.998517255441856e-06, 9.998517475262407e-06, 9.998517695017785e-06, 9.998517914708028e-06, 9.998518134333158e-06, 9.998518353893206e-06, 9.998518573388203e-06, 9.998518792818177e-06, 9.998519012183156e-06, 9.998519231483169e-06, 9.998519450718245e-06, 9.998519669888413e-06, 9.9985198889937e-06, 9.99852010803414e-06, 9.998520327009757e-06, 9.99852054592058e-06, 9.99852076476664e-06, 9.998520983547966e-06, 9.998521202264581e-06, 9.998521420916523e-06, 9.998521639503812e-06, 9.998521858026483e-06, 9.99852207648456e-06, 9.998522294878076e-06, 9.998522513207054e-06, 9.998522731471528e-06, 9.998522949671524e-06, 9.998523167807072e-06, 9.998523385878197e-06, 9.998523603884934e-06, 9.998523821827306e-06, 9.998524039705342e-06, 9.998524257519071e-06, 9.998524475268525e-06, 9.998524692953727e-06, 0.0], [0.0, 1.6002417009702357e-05, 1.6002416644636513e-05, 1.600241627968093e-05, 1.6002415914835562e-05, 1.6002415550100352e-05, 1.600241518547526e-05, 1.6002414820960226e-05, 1.600241445655521e-05, 1.6002414092260153e-05, 1.6002413728075013e-05, 1.6002413363999737e-05, 1.6002413000034274e-05, 1.6002412636178577e-05, 1.6002412272432593e-05, 1.6002411908796274e-05, 1.6002411545269573e-05, 1.6002411181852435e-05, 1.6002410818544815e-05, 1.6002410455346662e-05, 1.600241009225793e-05, 1.600240972927856e-05, 1.6002409366408512e-05, 1.6002409003647733e-05, 1.6002408640996177e-05, 1.6002408278453787e-05, 1.6002407916020522e-05, 1.6002407553696327e-05, 1.6002407191481156e-05, 1.6002406829374957e-05, 1.6002406467377687e-05, 1.6002406105489288e-05, 1.600240574370972e-05, 1.6002405382038922e-05, 1.6002405020476857e-05, 1.600240465902347e-05, 1.6002404297678717e-05, 1.600240393644254e-05, 1.6002403575314897e-05, 1.6002403214295737e-05, 1.6002402853385013e-05, 1.6002402492582673e-05, 1.600240213188867e-05, 1.6002401771302957e-05, 1.600240141082548e-05, 1.6002401050456198e-05, 1.6002400690195057e-05, 1.6002400330042005e-05, 1.6002399969997003e-05, 1.600239961005999e-05, 1.6002399250230932e-05, 1.600239889050977e-05, 1.6002398530896455e-05, 1.6002398171390946e-05, 1.600239781199319e-05, 1.6002397452703135e-05, 1.600239709352074e-05, 1.600239673444595e-05, 1.6002396375478725e-05, 1.6002396016619007e-05, 1.6002395657866757e-05, 1.6002395299221914e-05, 1.6002394940684445e-05, 1.600239458225429e-05, 1.600239422393141e-05, 1.6002393865715745e-05, 1.600239350760726e-05, 1.60023931496059e-05, 1.6002392791711615e-05, 1.600239243392436e-05, 1.600239207624409e-05, 1.6002391718670752e-05, 1.60023913612043e-05, 1.6002391003844686e-05, 1.6002390646591864e-05, 1.600239028944578e-05, 1.6002389932406392e-05, 1.600238957547365e-05, 1.600238921864751e-05, 1.6002388861927918e-05, 1.600238850531483e-05, 1.6002388148808197e-05, 1.6002387792407974e-05, 1.600238743611411e-05, 1.600238707992656e-05, 1.6002386723845272e-05, 1.6002386367870207e-05, 1.6002386012001308e-05, 1.6002385656238532e-05, 1.6002385300581832e-05, 1.600238494503116e-05, 1.6002384589586465e-05, 1.6002384234247708e-05, 1.6002383879014832e-05, 1.60023835238878e-05, 1.6002383168866553e-05, 1.6002382813951054e-05, 1.6002382459141248e-05, 1.6002382104437094e-05, 1.6002381749838538e-05, 1.6002381395345543e-05, 1.600238104095805e-05, 1.600238068667602e-05, 1.6002380332499405e-05, 1.6002379978428154e-05, 1.6002379624462223e-05, 1.600237927060157e-05, 1.6002378916846136e-05, 1.6002378563195884e-05, 1.6002378209650762e-05, 1.6002377856210727e-05, 1.6002377502875727e-05, 1.6002377149645722e-05, 1.6002376796520658e-05, 1.6002376443500494e-05, 1.600237609058518e-05, 1.600237573777467e-05, 1.600237538506892e-05, 1.6002375032467877e-05, 1.60023746799715e-05, 1.000148395473734e-05, 1.0001483734557845e-05, 1.0001483514443683e-05, 1.0001483294394816e-05, 1.000148307441122e-05, 1.0001482854492864e-05, 1.0001482634639722e-05, 1.0001482414851762e-05, 1.0001482195128955e-05, 1.0001481975471272e-05, 1.0001481755878686e-05, 1.0001481536351166e-05, 1.0001481316888685e-05, 1.0001481097491212e-05, 1.000148087815872e-05, 1.000148065889118e-05, 1.0001480439688561e-05, 1.0001480220550836e-05, 1.0001480001477977e-05, 1.0001479782469951e-05, 1.0001479563526735e-05, 1.0001479344648297e-05, 1.000147912583461e-05, 1.000147890708564e-05, 1.0001478688401366e-05, 1.0001478469781754e-05, 1.0001478251226778e-05, 1.0001478032736408e-05, 1.0001477814310616e-05, 1.000147759594937e-05, 1.000147737765265e-05, 1.0001477159420416e-05, 1.0001476941252649e-05, 1.0001476723149315e-05, 1.0001476505110388e-05, 1.0001476287135838e-05, 1.0001476069225638e-05, 1.0001475851379757e-05, 1.000147563359817e-05, 1.0001475415880845e-05, 0.0])',
    'N8 _basal_solve':
        '[2053.1026414032567, 2052.5489460161366, 2051.9989565883516, 2051.4524569758314, 2050.9094279222763, 2050.369737080002, 2049.833193455513, 2049.2996578681805, 2048.7690522571133, 2048.2412364846296, 2047.7160037750657, 2047.1953982934597, 2046.8037115730897, 2046.7882501954077, 2046.7811432249603, 2046.7761709679373, 2046.7731592401883, 2046.7720472919339, 2046.7727900622074, 2046.7753169117643, 2046.7795668227895, 2046.7854858527248, 2046.79302238423, 2046.8021080763665, 2046.8126858040646, 2046.824707042921, 2046.8381097196884, 2046.8528334970451, 2046.868823506078, 2046.886031056857, 2046.9043909792579, 2046.9238476882417, 2046.9443502595993, 2046.9658421516722, 2046.9882644641832, 2047.011562467468, 2047.035687279206, 2047.0605780271449, 2047.0861801441674, 2047.1124410513287, 2047.1392957290595]',
}


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


def refuses(fn, site: str):
    """(True, message) when fn() raises sm.Refused naming `site`; (False, what happened) otherwise."""
    try:
        got = fn()
    except sm.Refused as e:
        return site in str(e), str(e)[:120]
    except Exception as e:                          # noqa: BLE001 — any other exception is not the named refusal
        return False, f"{type(e).__name__}: {str(e)[:100]}"
    return False, f"no refusal: returned {str(got)[:80]}"


def twin(key: str, value) -> None:
    """The finite twin: equal to the 0c05bb5a value (repr), or recorded in --pins mode."""
    r = repr(value)
    if PINS_MODE:
        pins_out[key] = r
        return
    check(f"{key} — finite twin equals 0c05bb5a", PINS.get(key) == r, "" if PINS.get(key) == r else f"{r[:80]}")


ta.reset_stats()                       # the ALE mode's counters, as ta.run sets them
hp.reset_stats()
prof = ss.mars_profile(Path(__file__).resolve().parent / "bodies" / "mars.yaml")
G = prof.gravity(prof.radius_m)
LAYER = dict(d_d=st.D_D_M, k_d=4.0, lambda_d=14.373, fe_mean=96.97, fe_top=94.1306, nodes=41, melting=True)
STATE = (2158.1024424461625, 1815.5593199821958, 80e3, 20e3)
T_GYR, GRAD = 1.0, -0.02

s2 = ts.samuel_stack(lam=20.0, profile=prof, g=G)
s2.opt["melt_rule"] = "exact"
f0 = ts.state_terms(s2, *STATE, T_GYR, GRAD)
R_TOP = s2.r_p - STATE[2] - f0["delta_u"]
R_BOT = s2.r_base + f0["delta_b"]
D_REF = sm.crust_reference_thickness(s2.r_p, s2.r_c, s2.body["crust_reference_fraction"])
MKW = dict(d_cr=STATE[3], d_ref=D_REF, delta_t_sol=s2.body["delta_t_sol"],
           extraction_below_pa=s2.body["melt_extraction_below_pa"], shells=s2.opt["melt_shells"],
           curves=s2.body["curves"])
P_X = s2.body["melt_extraction_below_pa"]
import samuel_lid as sl                # noqa: E402
LID = sl.LidGrid(s2.lid.params["nodes"], r_p=s2.r_p, t_s=s2.body["t_surface"], rho_m=s2.mantle.params["rho"],
                 c_m=s2.mantle.params["cp"], k_m=s2.mantle.params["k"], rho_cr=s2.lid.params["rho_crust"],
                 c_cr=s2.lid.params["cp_crust"], k_cr=s2.lid.params["k_crust"])     # as thermal_ale._run builds it


def melt(t_m=STATE[1], t_b=f0["t_b"], pressure=s2.melt_p):
    return melt_exact.melt_integrals(t_m, t_b, R_TOP, R_BOT, pressure, **MKW)


# ── N1–N3: melt_exact ────────────────────────────────────────────────────────────────────────────────────────────
print("  N1–N3 melt_exact.melt_integrals")
twin("N1-N3 melt_integrals", melt())
check("N1–N3 setup — the extraction pressure lies inside the shell (a cut is bisected)",
      s2.melt_p(R_TOP) < P_X < s2.melt_p(R_BOT), f"P(top) {s2.melt_p(R_TOP):.4g} · P_x {P_X:.4g} · P(bot) {s2.melt_p(R_BOT):.4g}")
r_cut = R_BOT
lo_, hi_ = R_BOT, R_TOP
for _ in range(200):                                 # the radius of P_x on this profile (the cut the bisection finds)
    mid = 0.5 * (lo_ + hi_)
    lo_, hi_ = (mid, hi_) if s2.melt_p(mid) > P_X else (lo_, mid)
r_cut = 0.5 * (lo_ + hi_)


def p_nan_window(r):                                 # NaN within 1 m of the cut: only the bisection's late midpoints
    return NAN if abs(r - r_cut) < 1.0 else s2.melt_p(r)


if not PINS_MODE:
    ok, msg = refuses(lambda: melt(pressure=p_nan_window), "melt_exact.bisect_root")
    check("N1 — a NaN probe inside the cut bisection refuses by name (melt_exact.bisect_root)", ok, msg)
    ok, msg = refuses(lambda: melt(t_m=NAN), "melt_exact.add")
    check("N2 — a NaN temperature at a piece's ends refuses by name (melt_exact.add)", ok, msg)
    ok, msg = refuses(lambda: melt(pressure=lambda r: NAN if r == R_BOT else s2.melt_p(r)), "melt_exact.cuts")
    check("N3 — a NaN pressure at a shell end refuses by name (melt_exact.cuts)", ok, msg)


# ── N4: thermal_ale._radius_at ───────────────────────────────────────────────────────────────────────────────────
class StubP:
    """melt_p only: a linear pressure, NaN where `nan_at` says."""
    def __init__(self, nan_at=lambda r: False):
        self.nan_at = nan_at

    def melt_p(self, r):
        return NAN if self.nan_at(r) else (3.39e6 - r) * 1.3e4


print("  N4 thermal_ale._radius_at")
P4 = (3.39e6 - 2.7e6) * 1.3e4
twin("N4 _radius_at", ta._radius_at(StubP(), P4, 3.2e6, 2.0e6))
if not PINS_MODE:
    ok, msg = refuses(lambda: ta._radius_at(StubP(lambda r: r == 2.0e6), P4, 3.2e6, 2.0e6), "thermal_ale._radius_at")
    check("N4 — a NaN bracket end refuses by name, not «outside the shell» (None)", ok, msg)
    ok, msg = refuses(lambda: ta._radius_at(StubP(lambda r: abs(r - 2.7e6) < 1.0), P4, 3.2e6, 2.0e6),
                      "thermal_ale._radius_at")
    check("N4 — a NaN midpoint inside the bisection refuses by name", ok, msg)

# ── N5: thermal_ale.event_signs ──────────────────────────────────────────────────────────────────────────────────
print("  N5 thermal_ale.event_signs")
s2._ale_state = {"grad": GRAD, "tb": None, "th": None}
real_terms = ta.state_terms


def signs_with(override: dict, y=STATE):
    # the terms are the finite STATE's own (with `override`), so a NaN in y reaches event_signs' own check, not
    # state_terms' (which would refuse first, through melt_exact)
    ta.state_terms = lambda s, *a, **k: {**real_terms(s, *STATE, *a[4:], **k), **override}
    try:
        return ta.event_signs(s2, list(y), T_GYR, 1.0)
    finally:
        ta.state_terms = real_terms


twin("N5 event_signs", signs_with({}))
if not PINS_MODE:
    for key in ("stefan", "t_b", "delta_u", "delta_b"):
        ok, msg = refuses(lambda key=key: signs_with({key: NAN}), "thermal_ale.")
        check(f"N5 — a NaN {key} refuses by name, never a False sign", ok, msg)
    ok, msg = refuses(lambda: signs_with({}, y=(STATE[0], STATE[1], STATE[2], NAN)), "thermal_ale.event_signs")
    check("N5 — a NaN D_cr in the state refuses by name", ok, msg)

# ── N6: hop_track.hump_sign ──────────────────────────────────────────────────────────────────────────────────────
print("  N6 hop_track.hump_sign")
root = ft.Root(100.0, dx=1.0, lo=50.0, hi=150.0)
twin("N6 hump_sign", hp.hump_sign(lambda x: x - 110.0, root))
if not PINS_MODE:
    got = hp.hump_sign(lambda x: NAN, root)
    check("N6 — a NaN midpoint gives 0.0 («no hump»), not −1.0", got == 0.0, repr(got))
    lost = hp.lost(lambda x: x - 110.0, ft.Root(100.0, dx=1.0, lo=50.0, hi=150.0, g=0.0), "δ_b")
    check("N6 — lost() reads r.g = 0.0 as no fold (Lost(False))", lost.fold is False, repr(lost.fold))

# ── N7: thermal_ale.lid_coeffs ───────────────────────────────────────────────────────────────────────────────────
print("  N7 thermal_ale.lid_coeffs")
twin("N7 lid_coeffs", ta.lid_coeffs(LID, STATE[2], STATE[3], 1e-8, 5e-8))
if not PINS_MODE:
    ok, msg = refuses(lambda: ta.lid_coeffs(LID, STATE[2], NAN, 1e-8, 5e-8), "thermal_ale.lid_coeffs")
    check("N7 — a NaN D_cr refuses by name, not an all-crust lid", ok, msg)
    ok, msg = refuses(lambda: ta.lid_coeffs(LID, NAN, STATE[3], 1e-8, 5e-8), "thermal_ale.lid_coeffs")
    check("N7 — a NaN D_l refuses by name", ok, msg)

# ── N8: thermal_ale._basal_solve ─────────────────────────────────────────────────────────────────────────────────
print("  N8 thermal_ale._basal_solve")
s4 = ts.samuel_stack(lam=10.0, profile=prof, g=G, model="bml", layer=LAYER)
ts.state_terms(s4, *STATE, T_GYR, GRAD)            # the basal grid starts inside the first state_terms
lg = s4.layer_grid
t_mid = [0.5 * (a + b) for a, b in zip(lg.t_sol, lg.t_liq)]           # inside the melting interval: φ is live
rhs = ta._basal_energy(lg, t_mid, ta._basal_phi(lg, t_mid))
B_ARGS = (lg, rhs, 1e12, t_mid[0], t_mid[-1], t_mid)
check("N8 setup — the plate 4 basal grid melts (latent set)", lg.latent is not None, repr(lg.latent))
twin("N8 _basal_solve", ta._basal_solve(*B_ARGS))
if not PINS_MODE:
    real_tri = lay._solve_tridiagonal

    def tri_nan(*a, **k):                            # a NaN at the second interior node, not the first difference
        x = real_tri(*a, **k)
        x[2] = NAN
        return x
    lay._solve_tridiagonal = tri_nan
    try:
        ok, msg = refuses(lambda: ta._basal_solve(*B_ARGS), "thermal_ale._basal_solve")
    finally:
        lay._solve_tridiagonal = real_tri
    check("N8 — a NaN node after the solve refuses by name, never «converged»", ok, msg)

# ── N9: thermal_ale._run's step over τ ───────────────────────────────────────────────────────────────────────────
print("  N9 thermal_ale._run step")
if not PINS_MODE:
    s9 = ts.samuel_stack(lam=20.0, profile=prof, g=G)
    s9.body["age_gyr"] = s9.body["t_initial_gyr"] + 0.002
    real_tau = ta._tau_s
    ta._tau_s = lambda y, f: NAN
    try:
        out9 = ta.run(s9, 5.0)
    finally:
        ta._tau_s = real_tau
    check("N9 — a NaN τ refuses by name, never a step at cap", "thermal_ale._run.tau" in str(out9.get("refused")),
          str(out9.get("refused"))[:120])

# ── already guarded (plan §1): one planted line each ─────────────────────────────────────────────────────────────
if not PINS_MODE:
    print("  guarded sites (no change)")
    check("hop_track.bisect — a NaN probe returns None (nan_safe)",
          hp.bisect(lambda x: NAN if x > 0.4 else x - 0.7, 0.0, 1.0, -0.7) is None)
    check("hop_track.changes_sign — a NaN end is no sign change", not hp.changes_sign(NAN, 1.0)
          and not hp.changes_sign(-1.0, NAN))
    check("hop_track.checked — a NaN residual refuses the root (None)", hp.checked(lambda x: NAN, 1.0) is None)
    lo2 = hp.lost(lambda x: NAN, ft.Root(100.0, dx=1.0, lo=50.0, hi=150.0, g=1.0), "δ_b")
    check("hop_track.lost — a NaN on the hump is no fold (Lost(False))", lo2.fold is False, repr(lo2.fold))
    real_ls = ta._lid_solve
    ta._lid_solve = lambda *a, **k: [NAN] * LID.n
    try:
        f_lid = {**f0, "ddl": 1e-9, "lid_gradient": GRAD}
        try:
            ta._lid_stage(s2, LID, [0.0] * LID.n, 1.0, list(STATE), T_GYR, f_lid)
            lid_ok, lid_msg = False, "no Lost"
        except ft.Lost as e:
            lid_ok, lid_msg = e.equation == "Ḋ_l" and e.fold is False, f"Lost({e.equation}, {e.fold})"
    finally:
        ta._lid_solve = real_ls
    check("thermal_ale._lid_stage — a NaN secant never converges: Lost(«Ḋ_l», False)", lid_ok, lid_msg)
    print("  (hop_track.switch_branch's residual — `not (abs(fu) <= EPS …)` refuses on NaN — needs a fold state; not "
          "planted here, read in plan §1)")

if PINS_MODE:
    print(json.dumps(pins_out, indent=1, sort_keys=True))
    sys.exit(0)
print(f"test_d2_nan — {'all passed' if fails == 0 else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
