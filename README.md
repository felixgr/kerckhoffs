### Automatic Identification of Cryptographic Primitives in Software

Diploma/Master Thesis of Felix Gröbert

February 7, 2010

In this thesis we research and implement methods to detect cryptographic algorithms
and their parameters in software. Based on our observations on cryptographic code,
we point out several inherent characteristics to design signature-based and generic
identification methods. Using dynamic binary instrumentation, we record instructions
of a program during runtime and create a fine-grained trace. We implement a
trace analysis tool, which also provides methods to reconstruct high-level information
from a trace, for example control flow graphs or loops, to detect cryptographic
algorithms and their parameters. Using the results of this work, encrypted data, sent
by a program for example, may be decrypted and used by an analyst to gain further
insight on the behavior of the analyzed binary executable.

![Auguste Kerckhoffs](http://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Kerkhoffs.jpg/220px-Kerkhoffs.jpg "Sup?")


Keywords: Code Analysis, Dynamic Binary Analysis, Instrumentation, Code Heuristics, Code Signatures, Applied Cryptography


Also published in [RAID'11](https://scholar.google.de/citations?view_op=view_citation&hl=en&user=Uq29m54AAAAJ&citation_for_view=Uq29m54AAAAJ:u5HHmVD_uO8C)
 and [27c3](http://events.ccc.de/congress/2010/Fahrplan/events/4160.en.html)

Thesis [Google Scholar Link](https://scholar.google.de/citations?view_op=view_citation&hl=en&user=Uq29m54AAAAJ&citation_for_view=Uq29m54AAAAJ:u-x6o8ySG0sC)

Bibtex:

```
@mastersthesis{groebert2010,
Author = {Felix Gr{\"o}bert},
Title = {{Automatic Identification of Cryptographic Primitives in Software}},
School = {Ruhr-University Bochum, Germany},
Type = {Diplomarbeit},
Year = {2010}
}

@incollection{grobert2011automated,
title={Automated Identification of Cryptographic Primitives in Binary Programs},
author={Gr{\"o}bert, Felix and Willems, Carsten and Holz, Thorsten},
booktitle={Recent Advances in Intrusion Detection},
pages={41--60},
year={2011},
publisher={Springer}
}
```
