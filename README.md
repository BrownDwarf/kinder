kinder
---

A simple project to derive periods and amplitudes for K2 lightcurves.

We derive **periods** using the [multi-term Lomb-Scargle periodogram](http://www.astroml.org/book_figures/chapter10/fig_LS_double_eclipse.html).

We derive **amplitudes** with [linear regression](https://speakerdeck.com/dfm/pyastro16) with a simultaneous underlying polynomial to account for calibration artifacts.  We set the complexity of the polynomial through [leave N out cross-validation](https://youtu.be/uaztY3Lbr4A?t=50m26s).

In cases with unusually noisy lightcurves we assign periods and amplitudes from human visual pattern recognition.


### Authors:  
- Michael Gully-Santiago (Kavli Institute for Astronomy & Astrophysics)
- Greg Herczeg (Kavli Institute for Astronomy & Astrophysics)
- CS19 Hack Day participants?


### License
MIT
