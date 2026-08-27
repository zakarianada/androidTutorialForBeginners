import math, random, wave, struct
SR=44100; D=30.0; N=int(SR*D); L=[0.0]*N; R=[0.0]*N; random.seed(27)
def add(i,v,pan=0.0):
    if 0<=i<N:
        lg=math.sqrt((1-pan)*0.5); rg=math.sqrt((1+pan)*0.5); L[i]+=v*lg; R[i]+=v*rg
def tone(start,dur,f0,f1=None,amp=.2,decay=5.0,pan=0.0):
    s=int(start*SR); n=int(dur*SR); ph=0.0
    for j in range(n):
        u=j/max(1,n-1); f=f0 if f1 is None else f0*((f1/f0)**u); ph+=2*math.pi*f/SR
        env=math.exp(-decay*(j/SR)); add(s+j,math.sin(ph)*env*amp,pan)
def noise(start,dur,amp=.08,decay=15.0,pan=0.0):
    s=int(start*SR); n=int(dur*SR); prev=0.0
    for j in range(n):
        raw=random.uniform(-1,1); hp=raw-.82*prev; prev=raw; env=math.exp(-decay*(j/SR)); add(s+j,hp*env*amp,pan)
def whoosh(start,dur=.32,amp=.09,pan=0.0):
    s=int(start*SR); n=int(dur*SR); ph=0.0
    for j in range(n):
        u=j/max(1,n-1); env=math.sin(math.pi*u)**1.7; f=280+5200*u*u; ph+=2*math.pi*f/SR
        add(s+j,(.65*random.uniform(-1,1)+.35*math.sin(ph))*env*amp,pan)
for i in range(N):
    t=i/SR; v=.028*math.sin(2*math.pi*55*t)+.016*math.sin(2*math.pi*82.41*t); L[i]+=v; R[i]+=v
beat=60/132.0; x=0.0; b=0
while x<D:
    tone(x,.28,145,45,.42,11); 
    if b%2==1: noise(x,.18,.12,18); tone(x,.12,190,None,.055,24)
    noise(x,.055,.025,55,-.25); noise(x+beat/2,.055,.025,55,.25); b+=1; x+=beat
for idx,t in enumerate([2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5]):
    whoosh(t-.24,.28,.07,-.35 if idx%2 else .35); tone(t,.42,82,36,.34,8.5); noise(t,.12,.10,22)
notes=[110,123.47,146.83,164.81,196,220]
for j in range(14): tone(20+j*.68,.30,notes[j%len(notes)],None,.055,7,-.35 if j%2==0 else .35)
whoosh(28.95,.55,.13); tone(29.25,.72,72,29,.50,4)
fi=int(.18*SR); fo=int(.45*SR); peak=1e-9
for i in range(N):
    g=i/max(1,fi) if i<fi else (max(0.0,(N-i)/fo) if i>N-fo else 1.0)
    L[i]=math.tanh(L[i]*1.25)*g; R[i]=math.tanh(R[i]*1.25)*g; peak=max(peak,abs(L[i]),abs(R[i]))
sc=.92/peak
with wave.open('soundtrack.wav','wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); frames=bytearray()
    for l,r in zip(L,R): frames+=struct.pack('<hh',int(max(-1,min(1,l*sc))*32767),int(max(-1,min(1,r*sc))*32767))
    wf.writeframes(frames)
print('soundtrack.wav created')