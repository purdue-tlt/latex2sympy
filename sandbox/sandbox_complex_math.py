from sympy import *
from latex2sympy.latex2sympy import process_sympy
from latex2sympy.lib import parseToJson

MAX_PREC = 631

latex_strings = [
    # '4+3I',
    # '4.1+3.2I',
    # '50(\\cos(60\\frac{\\pi}{180})+I\\sin(60\\frac{\\pi}{180}))',
    # '50e^{I60\\frac{\\pi}{180}}'
    '3+4\\imaginaryI ',
    '-3-4\\imaginaryI',
    '3+\\imaginaryI 4',
    '3+\\imaginaryJ 4',
    '50\\angle 2\\pi ',
    '50\\angle 2.1\\pi ',
    '50\\angle \\frac{\\pi}{4} ',
    '50\\angle -3.14',
    '5\\sqrt{2}\\angle 60\\degree '
]

for latex in latex_strings:
    print('json => ', parseToJson(latex))
    expr = process_sympy(latex)
    print('latex => ', latex)
    print('sympy =>', expr)
    print('srepr =>', srepr(expr))
    print('as_real_imag =>', expr.as_real_imag())
    print('re =>', re(expr))
    print('im =>', im(expr))
    print('arg =>', arg(expr))
    print('Abs =>', Abs(expr))
    print('evalf =>', expr.evalf(chop=True))
    print('====================================')


def compute_expr(expr):
    evaluated_value = expr.doit().evalf(chop=True, n=MAX_PREC).round(15)
    try:
        rational_value = Rational(str(evaluated_value))
        return rational_value
    except Exception as e:
        # print(e)
        return evaluated_value


print('math example problem')
print('====================================')

# enter the variables here
# ------------------------

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

print('variables:', [(key, value) for key, value in variable_values.items()])

# enter the calculations here
# ---------------------------

# Calculations to set up problem variables - same as Skill Builder 3.1.8
# $P=$PT*1E6/3;
# $P=2666666.66666667
P_expr = process_sympy('\\variable{PT}*1E6/3', variable_values=variable_values)
P = compute_expr(P_expr)
print('P =', P, ', evalf() =>', P.evalf(), ', expected = 2666666.66666667')

# $VT=$VLL/sqrt(3)*1E3;
# $VT=5773.50269189626
VT_expr = process_sympy('\\variable{VLL}/\\sqrt{3}*1E3', variable_values=variable_values)
VT = compute_expr(VT_expr)
print('VT =', VT, ', evalf() =>', N(VT, 15), ', expected = 5773.50269189626')

# $phirad=acos($pf);
# $phirad=0.722734247813416
phirad_expr = process_sympy('\\arccos{\\variable{pf}}', variable_values=variable_values)
phirad = compute_expr(phirad_expr)
print('phirad =', phirad, ', evalf() =>', N(phirad, 15), ', expected = 0.722734247813416')

# $Imag=$P/($VT*$pf);
# $Imag=615.840287135601
Imag_expr = process_sympy('\\frac{\\variable{P}}{\\variable{VT}\\variable{pf}}', variable_values=variable_values | {'P': P, 'VT': VT})
Imag = compute_expr(Imag_expr)
print('Imag =', Imag, ', evalf() =>', N(Imag, 15), ', expected = 615.840287135601')

# $I=cplxe($Imag,-$phirad);
# $I=[615.840287135601,-0.722734247813416]
# I_var = process_sympy('\\variable{Imag}*(\\cos{-\\variable{phirad}}+I*\\sin{-\\variable{phirad}})', variable_values=variable_values | {'Imag': Imag, 'phirad': phirad})
I_expr = process_sympy('\\variable{Imag}\\angle -\\variable{phirad}', variable_values=variable_values | {'Imag': Imag, 'phirad': phirad})
I_var = compute_expr(I_expr)
print('I_var =', I_expr, ', evalf() =>', N(I_var, 15), ', expected = [615.840287135601,-0.722734247813416]')

# $VR=$I*$Ra;
VR_expr = process_sympy('\\variable{I}*\\variable{Ra}', variable_values=variable_values | {'I': I_var})
VR = compute_expr(VR_expr)
print('VR =', VR, ', evalf() =>', N(VR, 15))

# $VRmag=abs($VR);
# $VRmag=123.16805742712
VRmag_expr = process_sympy('|\\variable{VR}|', variable_values=variable_values | {'VR': VR})
VRmag = compute_expr(VRmag_expr)
print('VRmag =', VRmag, ', evalf() =>', N(VRmag, 15), ', expected = 123.16805742712')

# $VRphase=arg($VR)*180/pi;
# $VRphase=-41.4096221092709
VRphase_expr = process_sympy('\\operatorname{Arg}(\\variable{VR})\\frac{180}{\\pi }', variable_values=variable_values | {'VR': VR})
VRphase = compute_expr(VRphase_expr)
print('VRphase =', VRphase, ', evalf() =>', N(VRphase, 15), ', expected = -41.4096221092709')

# $VXS=$I*i*$Xs;
# $VXS=224.037033975619+254.034118443435i
VXS_expr = process_sympy('\\variable{I}\\imaginaryI \\variable{Xs}', variable_values=variable_values | {'I': I_var})
VXS = compute_expr(VXS_expr)
print('VXS =', VXS, ', evalf() =>', N(VXS, 15), ', expected = 224.037033975619+254.034118443435i')

# $VXSmag=abs($VXS);
# $VXSmag=338.71215792458
VXSmag_expr = process_sympy('|\\variable{VXS}|', variable_values=variable_values | {'VXS': VXS})
VXSmag = compute_expr(VXSmag_expr)
print('VXSmag =', VXSmag, ', evalf() =>', N(VXSmag, 15), ', expected = 338.71215792458')

# $VXSphase=arg($VXS)*180/pi;
# $VXSphase=48.5903778907291
VXSphase_expr = process_sympy('\\operatorname{Arg}(\\variable{VXS})\\frac{180}{\\pi }', variable_values=variable_values | {'VXS': VXS})
VXSphase = compute_expr(VXSphase_expr)
print('VXSphase =', VXSphase, ', evalf() =>', N(VXSphase, 15), ', expected = 48.5903778907291')

# $Ef=$VT+$VR+$VXS;
# $Ef=6089.91576894222+172.566106088665i
Ef_expr = process_sympy('\\variable{VT}+\\variable{VR}+\\variable{VXS}', variable_values=variable_values | {'VT': VT, 'VR': VR, 'VXS': VXS})
Ef = compute_expr(Ef_expr)
print('Ef =', Ef, ', evalf() =>', N(Ef, 15), ', expected = 6089.91576894222+172.566106088665i')

# $Efmag=abs($Ef);
# $Efmag=6092.3602268564
Efmag_expr = process_sympy('|\\variable{Ef}|', variable_values=variable_values | {'Ef': Ef})
Efmag = compute_expr(Efmag_expr)
print('Efmag =', Efmag, ', evalf() =>', N(Efmag, 15), ', expected = 6092.3602268564')

# $Efphase=arg($Ef)*180/pi;
# $Efphase=1.62312006884331
Efphase_expr = process_sympy('\\operatorname{Arg}(\\variable{Ef})\\frac{180}{\\pi }', variable_values=variable_values | {'Ef': Ef})
Efphase = compute_expr(Efphase_expr)
print('Efphase =', Efphase, ', evalf() =>', N(Efphase, 15), ', expected = 1.62312006884331')

# $VLLNL=sqrt(3)*$Efmag;
# $VLLNL=10552.2774509271
VLLNL_expr = process_sympy('\\sqrt{3}*\\variable{Efmag}', variable_values=variable_values | {'Efmag': Efmag})
VLLNL = compute_expr(VLLNL_expr)
print('VLLNL =', VLLNL, ', evalf() =>', N(VLLNL, 15), ', expected = 10552.2774509271')

# New Claculatins for Skill Builder 3.1.9
# ---------------------------

# $phirad2=acos($pf2);
# $phirad2=0.402715841580661
phirad2_expr = process_sympy('\\arccos{\\variable{pf2}}', variable_values=variable_values)
phirad2 = compute_expr(phirad2_expr)
print('phirad2 =', phirad2, ', evalf() =>', N(phirad2, 15), ', expected = 0.402715841580661')

# $I2=cplxe($Imag,-$phirad2);
# $I2=[615.840287135601,-0.402715841580661]
# I2 = process_sympy('\\variable{Imag}*(\\cos{-\\variable{phirad2}}+I*\\sin{-\\variable{phirad2}})', variable_values=variable_values | {'Imag': Imag, 'phirad2': phirad2})
I2_expr = process_sympy('\\variable{Imag}\\angle -\\variable{phirad2}', variable_values=variable_values | {'Imag': Imag, 'phirad2': phirad2})
I2 = compute_expr(I2_expr)
print('I2 =', I2, ', evalf() =>', N(I2, 15), ', expected = [615.840287135601,-0.402715841580661]')

# $VXS2=$I2*i*$Xs;
# $VXS2=132.747513054755+311.615185290614i
VXS2_expr = process_sympy('\\variable{I2}\\imaginaryI \\variable{Xs}', variable_values=variable_values | {'I2': I2, 'Xs': Xs})
VXS2 = compute_expr(VXS2_expr)
print('VXS2 =', VXS2, ', evalf() =>', N(VXS2, 15), ', expected = 132.747513054755+311.615185290614i')

# $VT2=(($Efmag)**2-(Im($VXS2))**2)**0.5-Re($VXS2);
# $VT2=5951.6381675278
# VT2_expr = ((Efmag)**2 - (im(VXS2))**2)**0.5 - re(VXS2)
VT2_expr = process_sympy('(\\variable{Efmag}^{2} - \\operatorname{Im}(\\variable{VXS2})^{2})^{0.5} - \\operatorname{Re}(\\variable{VXS2})', variable_values=variable_values | {'Efmag': Efmag, 'VXS2': VXS2})
VT2 = compute_expr(VT2_expr)
print('VT2 =', VT2, ', evalf() =>', N(VT2, 15), ', expected = 5951.6381675278')

print('----------------------')

# $VLL2=$VT2*sqrt(3);
# $VLL2=10308.5396944243
VLL2_expr = process_sympy('\\variable{VT2}*\\sqrt{3}', variable_values=variable_values | {'VT2': VT2})
VLL2 = compute_expr(VLL2_expr)
print('VLL2 =', VLL2, ', evalf() =>', N(VLL2, 15), ', expected = 10308.5396944243')

# $VLL2ang=0;
VLL2ang = 0
print('VLL2ang =', VLL2ang, ', evalf() =>', N(VLL2ang, 15), ', expected = 0')

# $delta=acos(($VT2+Re($VXS2))/$Efmag)*180/pi;
# $delta=2.93187343130811
# delta_expr = acos((VT2 + re(VXS2)) / Efmag) * 180 / pi
delta_expr = process_sympy('\\arccos{\\frac{\\variable{VT2} + \\operatorname{Re}(\\variable{VXS2})}{\\variable{Efmag}}}\\frac{180}{\\pi }', variable_values=variable_values | {'VT2': VT2, 'Efmag': Efmag, 'VXS2': VXS2})
delta = compute_expr(delta_expr)
print('delta =', delta, ', evalf() =>', N(delta, 15), ', expected = 2.93187343130811')

# $VR_ans=($Efmag-$VT2)/$VT2*100;
# $VR_ans=2.36442564832618
VR_ans_expr = process_sympy('(\\variable{Efmag}-\\variable{VT2})/\\variable{VT2}*100', variable_values=variable_values | {'VT2': VT2, 'Efmag': Efmag})
VR_ans = compute_expr(VR_ans_expr)
print('VR_ans =', VR_ans, ', evalf() =>', N(VR_ans, 15), ', expected = 2.36442564832618')

# $Pmax=3*$VT2*$Efmag/$Xs;
# $Pmax=197779219.944474
Pmax_expr = process_sympy('3*\\variable{VT2}*\\variable{Efmag}/\\variable{Xs}', variable_values=variable_values | {'VT2': VT2, 'Efmag': Efmag})
Pmax = compute_expr(Pmax_expr)
print('Pmax =', Pmax, ', evalf() =>', N(Pmax, 15), ', expected = 197779219.944474')

# Other
# ----------------------

# $deg2rad=0.0174532925199433
# $pi=3.14159265358979
# $rad2deg=57.2957795130823
