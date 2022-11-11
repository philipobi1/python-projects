from sympy import *
from IPython.display import display,Latex
from itertools import product

def gauss(eq,values=None,eq_symbol='G',title='Fehlerbestimmung mit der Gauß-Fehlerfortpflanzungsformel'):
    display(Latex(f'$\\text{{ \\Large {title}}}$'))

    if values:
        values = dict(values)
        for sym,tup in dict(values).items():
            sym_l = str(latex(sym))
            delta_l = f'\\Delta {sym_l}'
            delta = Symbol(delta_l)

            display(Latex(f'${sym_l} = {tup[0]},\\quad{delta_l} = {tup[1]}$'))
            
            values[delta] = tup[1]
            values[sym] = tup[0]
    
    display(Latex(f'${eq_symbol}({",".join([latex(sym) for sym in eq.free_symbols])}) = {latex(eq)}' + (f' = {eq.evalf(subs=values)}$' if values else '$')))

    sum = 0
    
    for sym in eq.free_symbols:
        sym_l = latex(sym)
        partial = simplify(diff(eq,sym))
        
        display(Latex(r'$\frac{\partial %s}{\partial %s} = %s'%(eq_symbol,sym_l,latex(partial)) + (f' = {partial.evalf(subs=values)}$' if values else '$')))
        
        sum+= (partial*Symbol(f'\\Delta {sym_l}'))**2

    gauss_eq = simplify(sqrt(sum))

    gauss_formula = r'$\Delta %s(\vec x) = \sqrt{\sum_{i}(\left. \frac{\partial %s(\vec x)}{\partial x_i} \right|_{\vec x = \vec x_0} \Delta x_i)^2} = '%(eq_symbol,eq_symbol)
    display(Latex(gauss_formula + latex(gauss_eq) + (f' = {gauss_eq.evalf(subs=values)}$' if values else '$')))


def minmax(eq,values,eq_symbol='G',title='Fehlerbestimmung mit der Min-Max-Methode'):
    values = dict(values)
    display(Latex(f'$\\text{{\\Large {title}}}$'))
    
    errors = list()
    for sym,tup in dict(values).items():
        value,error = tup
        sym_l = str(latex(sym))
        delta_l = f'\\Delta {sym_l}'
        delta = Symbol(delta_l)

        display(Latex(f'${sym_l} = {value},\\quad{delta_l} = {error}$'))
        
        if error:
            errors.append(delta)
            eq = eq.subs(sym,sym+delta)
            values[delta] = error
        
        values[sym]=value

    result = eq.evalf(subs=values)
    display(Latex(f'${eq_symbol}({",".join([latex(sym) for sym in eq.free_symbols])}) = {latex(eq)} = {result}$'))

    if errors:
        min=max=(result,eq,list(zip(errors,(0,)*len(errors))))
        combinations = list(product([-1,1],repeat=len(errors)))
        for combination in combinations:
            error_comb = list(zip(errors,combination))
            new_eq = eq.subs({delta:a*delta for delta,a in error_comb})
            comb_result = new_eq.evalf(subs=values)
            tup = (comb_result,new_eq,error_comb)
            if comb_result < min[0]:
                min = tup
            if comb_result > max[0]:
                max = tup
        
        s = r', \quad'.join([latex(delta*a) for delta,a in min[2]])
        display(Latex(f'${{{eq_symbol}}}_{{min}} = {latex(min[1])} = {min[0]} \\quad (Kombination: {s})$'))
        
        s = r', \quad'.join([latex(delta*a) for delta,a in max[2]])
        display(Latex(f'${{{eq_symbol}}}_{{max}} = {latex(max[1])} = {max[0]} \\quad (Kombination: {s})$'))
            
        


    