#!/usr/bin/env python
# -*- coding: utf-8 -*-

def heapsort(a, n):
    for i in range((n/2), -1, -1):                
        ajuste(a, i, n)
    for i in range((n-1), -1, -1):                
        temp = a[i]
        a[i] = a[0]
        a[0] = temp
        ajuste(a,0,i);
		
def ajuste(a, i, n):
	aAux = a[i]
	j = 2*i
	while j < n:
		if (j < (n - 1) and a[j] < a[j+1]):
			j = j + 1
		if (aAux >= a[j]):
			return		
		a[j/2] = a[j]
		a[j] = aAux
		j = 2*j
	a[j/2] = aAux
	
a = [4, 1, 6, 7, 3, 4, 0]
heapsort(a, len(a))
print(a)