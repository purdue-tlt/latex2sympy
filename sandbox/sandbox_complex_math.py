from sympy import *
from latex2sympy.latex2sympy import process_sympy
# from latex2sympy.latex2antlrJson import parseToJson

# enter the variables here

# $PT=&random(8,12,1);
# $pf=&random(0.75,0.85,0.025);
# $VLL=&random(9,12,1);
# $Ra=&random(0.10,0.20,0.01);
# $Xs=&random(0.55,0.01,0.66);
# $pf2=&random(0.9,0.95,0.01);

# $PT=8
# $pf=0.75
# $VLL=10
# $Ra=0.2
# $Xs=0.55
# $pf2=0.92

PT = process_sympy('8')
pf = process_sympy('0.75')
VLL = process_sympy('10')
Ra = process_sympy('0.2')
Xs = process_sympy('0.55')
pf2 = process_sympy('0.92')

variable_values = {
    'PT': PT,
    'pf': pf,
    'VLL': VLL,
    'Ra': Ra,
    'Xs': Xs,
    'pf2': pf2
}

print('variables:', [(key, srepr(value)) for key, value in variable_values.items()])

# enter the calculations here

# Calculations to set up problem variables - same as Skill Builder 3.1.8
# $P=$PT*1E6/3;
# $P=2666666.66666667
P_expr = process_sympy('\\variable{PT}*1E6/3', variable_values=variable_values)
P = P_expr.doit().evalf()
print('P ', P)

# $VT=$VLL/sqrt(3)*1E3;
# $VT=5773.50269189626
VT_expr = process_sympy('\\variable{VLL}/\\sqrt{3}*1E3', variable_values=variable_values)
VT = VT_expr.doit().evalf()
print('VT =', VT)

# $phirad=acos($pf);
# $phirad=0.722734247813416
phirad_expr = process_sympy('\\arccos{\\variable{pf}}', variable_values=variable_values)
phirad = phirad_expr.doit().evalf()
print('phirad =', phirad)

# $Imag=$P/($VT*$pf);
# $Imag=615.840287135601
Imag_expr = process_sympy('\\frac{\\variable{P}}{\\variable{VT}\\variable{pf}}', variable_values=variable_values | {'P': P, 'VT': VT})
Imag = Imag_expr.doit().evalf()
print('Imag =', Imag)

# $I=cplxe($Imag,-$phirad);
# $I=[615.840287135601,-0.722734247813416]
# TODO
I_var = exp_polar(Imag, -phirad)
print('I_var =', I_var)

# $VR=$I*$Ra;
# $VR=2.36442564832618
VR_expr = process_sympy('\\variable{I}*\\variable{Ra}', variable_values=variable_values | {'I': I_var})
VR = VR_expr.doit().evalf()
print('VR =', VR)

# $VRmag=abs($VR);
# $VRmag=123.16805742712
VRmag_expr = process_sympy('|\\variable{VR}|', variable_values=variable_values | {'VR': VR})
VRmag = VRmag_expr.doit().evalf()
print('VRmag =', VRmag)

# $VRphase=arg($VR)*180/pi;
# $VRphase=-41.4096221092709
VRphase = arg(VR) * 180 / pi
print('VRphase =', VRphase)

# $VXS=$I*i*$Xs;
# $VXS=224.037033975619+254.034118443435i
VXS = I_var * I * Xs
print('VXS =', VXS)

# $VXSmag=abs($VXS);
# $VXSphase=arg($VXS)*180/pi;
# $Ef=$VT+$VR+$VXS;
# $Efmag=abs($Ef);
# $Efphase=arg($Ef)*180/pi;
# $VLLNL=sqrt(3)*$Efmag;

# New Claculatins for Skill Builder 3.1.9
# $phirad2=acos($pf2);
# $I2=cplxe($Imag,-$phirad2);
# $VXS2=$I2*i*$Xs;
# $VT2=(($Efmag)**2-(Im($VXS2))**2)**0.5-Re($VXS2);
# $VLL2=$VT2*sqrt(3);
# $VLL2ang=0;
# $delta=acos(($VT2+Re($VXS2))/$Efmag)*180/pi;
# $VR=($Efmag-$VT2)/$VT2*100;
# $Pmax=3*$VT2*$Efmag/$Xs;

# $Ef=6089.91576894222+172.566106088665i
# $Efmag=6092.3602268564
# $Efphase=1.62312006884331
# $I2=[615.840287135601,-0.402715841580661]
# $Pmax=197779219.944474
# $VLL2=10308.5396944243
# $VLL2ang=0
# $VLLNL=10552.2774509271
# $VT2=5951.6381675278
# $VXS2=132.747513054755+311.615185290614i
# $VXSmag=338.71215792458
# $VXSphase=48.5903778907291
# $deg2rad=0.0174532925199433
# $delta=2.93187343130811
# $phirad2=0.402715841580661
# $pi=3.14159265358979
# $rad2deg=57.2957795130823
