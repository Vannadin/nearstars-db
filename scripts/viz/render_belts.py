# 태양계 천체 방사선대 단면(스톡 vs 물리) PNG 렌더러 — 인게임 Kerbalism SDF 그대로 (위키 업로드용)
# SDF 알고리즘 출처: Kerbalism (github.com/Kerbalism/Kerbalism), src/Kerbalism/Radiation/Radiation.cs.
# 라이선스: Unlicense (퍼블릭 도메인) — 저작권 주장 없음, 출처 표기는 예의상.
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# ---- inferno colormap stops (matplotlib inferno, 10 anchors) ----
_ST = np.array([[0,0,4],[27,12,65],[74,12,107],[120,28,109],[165,44,96],
                [207,68,70],[237,105,37],[251,155,6],[247,209,61],[252,255,164]],float)
def inferno(t):
    t = np.clip(t,0,1)*9; i = np.floor(t).astype(int); f = (t-i)[...,None]
    i2 = np.minimum(i+1,9)
    return _ST[i]*(1-f)+_ST[i2]*f

def torus_sdf(x,y,z,B):
    px = x*np.where(x<0,B.get('ext',1),B.get('comp',1))
    q1 = np.sqrt((px*px+z*z)*B.get('dxy',1))-B['dist']
    d1 = np.sqrt(q1*q1+y*y)-B['rad']
    q2 = np.sqrt((px*px+z*z)*B.get('bdxy',1))-B.get('bdist',1e-4)
    d2 = np.sqrt(q2*q2+y*y)-B.get('brad',0)
    v = np.maximum(d1,-d2)
    if B.get('deform',0)>1e-3:
        v = v+np.sin(px*5)*np.sin(y*7)*np.sin(z*6)*B['deform']
    return v

def pause_sdf(x,y,z,P):
    px = x*np.where(x<0,P.get('ext',1),P.get('comp',1)); py = y*P.get('hscale',1)
    return np.sqrt(px*px+py*py+z*z)-P['rad']

def render(body, out, size=560, z=0.0):
    """body: {title, sub, R(halfwidth), tilt, inner{}, outer{}, pause{}}"""
    R = body['R']; tilt = np.radians(body.get('tilt',0))
    ca,sa = np.cos(tilt),np.sin(tilt)
    xs = (np.arange(size)-size/2)*(2*R/size)
    ys = (size/2-np.arange(size))*(2*R/size)
    X,Y = np.meshgrid(xs,ys)
    Z = np.full_like(X,z)
    Xr = X*ca - Y*sa; Yr = X*sa + Y*ca
    off = body.get('offset',0.0)          # geomagnetic_offset: dipole 중심을 자기축(+y_rot) 방향 이동
    Yr = Yr - off
    mag = np.sqrt(X*X+Y*Y+Z*Z)            # 바디 구는 지오메트릭 중심 기준(offset 무관)
    inner,outer,pause = body.get('inner'),body.get('outer'),body.get('pause')
    maxI = max(inner['radiation'] if inner and inner.get('on',True) else 0,
               outer['radiation'] if outer and outer.get('on',True) else 0, 1e-6)
    dose = np.zeros_like(X)
    for B,gdef in ((inner,3.3),(outer,2.2)):
        if not (B and B.get('on',True)): continue
        d = torus_sdf(Xr,Yr,Z,B); m=d<0
        dose[m]+=np.clip(B.get('grad',gdef)*(-d[m])/B['rad'],0,1)*B['radiation']
    img = np.zeros((size,size,3),float); img[:]=(5,7,13)
    if pause and pause.get('on',True):
        pd = pause_sdf(Xr,Yr,Z,pause)
        img[pd<0]=(10,16,30)
    m = dose>1e-4
    img[m]=inferno(dose[m]/maxI)
    if pause and pause.get('on',True):
        wpp=2*R/size
        img[np.abs(pd)<wpp*1.3]=(57,207,217)
    body_m = mag<1
    lit = np.clip(0.32+0.5*X,0.12,0.92)
    img[body_m]=np.stack([48*lit+18,58*lit+20,74*lit+24],-1)[body_m]
    im = Image.fromarray(np.clip(img,0,255).astype('uint8'),'RGB')
    dr = ImageDraw.Draw(im)
    c=size/2; ppr=size/(2*R)
    step = 1 if R<=4 else 2 if R<=10 else 5 if R<=25 else 10 if R<=60 else 20
    try: fnt=ImageFont.truetype("/System/Library/Fonts/Menlo.ttc",11); fbig=ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc",15)
    except: fnt=ImageFont.load_default(); fbig=fnt
    rr=step
    while rr<=R:
        dr.ellipse([c-rr*ppr,c-rr*ppr,c+rr*ppr,c+rr*ppr],outline=(255,255,255,30))
        dr.text((c+rr*ppr+2,c-13),str(rr),fill=(150,150,150),font=fnt); rr+=step
    dr.line([0,c,size,c],fill=(255,255,255,26)); dr.line([c,0,c,size],fill=(255,255,255,26))
    dr.text((10,8),body['title'],fill=(230,235,245),font=fbig)
    dr.text((10,30),body.get('sub',''),fill=(140,160,190),font=fnt)
    dr.text((size-96,size-20),"☀ star →",fill=(255,154,82),font=fnt)
    # 절대 강도 컬러바 (색은 이 바디 peak 기준 정규화 — 바디끼리 절대 비교하려면 이 숫자를 볼 것)
    def g(v): return f"{v:.0f}" if abs(v)>=10 else f"{v:.2f}".rstrip('0').rstrip('.')
    bx,by,bw,bh=10,size-46,150,9
    for i in range(bw):
        cr=inferno(i/(bw-1)); dr.line([(bx+i,by),(bx+i,by+bh)],fill=(int(cr[0]),int(cr[1]),int(cr[2])))
    dr.rectangle([bx,by,bx+bw,by+bh],outline=(120,120,120))
    dr.text((bx,by-13),"dose 0",fill=(150,160,175),font=fnt)
    dr.text((bx+bw-46,by-13),f"{g(maxI)} rad/h",fill=(247,209,61),font=fnt)
    parts=[]
    if inner and inner.get('on',True): parts.append(f"inner {g(inner['radiation'])}")
    if outer and outer.get('on',True): parts.append(f"outer {g(outer['radiation'])}")
    dr.text((bx,by+bh+2),("peak "+" · ".join(parts)+" rad/h" if parts else "no belt"),fill=(150,160,175),font=fnt)
    im.save(out); print("wrote",out)
    return out

if __name__=='__main__':
    # self-test: Earth (ROKerbalism earth model)
    earth={'title':'Earth (test)','sub':'R in R_body','R':7,'tilt':11,
      'inner':{'radiation':10.376,'grad':3.3,'dist':0.813,'rad':0.70,'dxy':0.572,'comp':1.01,'ext':1.0,'bdist':1e-4,'brad':0.915,'bdxy':0.5},
      'outer':{'radiation':2.214,'grad':2.2,'dist':2.6338,'rad':2.48,'dxy':0.7225,'comp':1.01,'ext':1.0,'bdist':1.4412,'brad':1.4875,'bdxy':0.7225},
      'pause':{'radiation':-0.01,'rad':15,'comp':1.5,'ext':0.075,'hscale':1.1}}
    d=os.path.dirname(os.path.abspath(__file__))
    render(earth, os.path.join(d,'_test_earth.png'))
