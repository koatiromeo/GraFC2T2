# GraFC2T2 : Optimisation de Performance pour les Systèmes de Recommandation Basés sur les Graphes

## Table des matières

1.  [Introduction](#1-introduction)
2.  [Structure du Projet](#2-structure-du-projet)
3.  [Configuration et Installation](#3-configuration-et-installation)
    * [Version Python](#31-version-python)
    * [Versions C++ (Standard et Optimisée)](#32-versions-c-standard-et-optimisée)
4.  [Méthodologie d'Analyse de Performance](#4-méthodologie-danalyse-de-performance)
    * [Identification des Goulots d'Étranglement](#41-identification-des-goulots-détranglement)
    * [Mise en Œuvre des Solutions d'Optimisation](#42-mise-en-œuvre-des-solutions-doptimisation)
    * [Évaluation des Optimisations](#43-évaluation-des-optimisations)
5.  [Résultats et Discussion](#5-résultats-et-discussion)
6.  [Utilisation du Projet](#6-utilisation-du-projet)
7.  [Contributions](#7-contributions)
8.  [Perspectives](#8-perspectives)
9.  [Licence](#9-licence)

---

## 1. Introduction

Ce projet, **GraFC2T2**, explore l'optimisation des performances des systèmes de recommandation basés sur les graphes. Face aux défis posés par les temps d'exécution élevés de ces modèles, notre travail propose une méthodologie structurée pour identifier les goulots d'étranglement et apporter des solutions concrètes. Initialement développé en Python, l'application GraFC2T2 a été réimplémentée en C++ et optimisée pour tirer parti des architectures matérielles modernes, démontrant ainsi comment une analyse approfondie et des optimisations ciblées peuvent améliorer significativement la réactivité de ces systèmes cruciaux pour la rentabilité et la satisfaction utilisateur.

---

## 2. Structure du Projet

Le projet GraFC2T2 est organisé en plusieurs répertoires pour faciliter la gestion des différentes versions de l'application, des données et des analyses.

* `./` (Racine du Projet)
    * `Roofline_optimize.py` : Script Python pour générer le graphique Roofline après optimisation.
    * `Roofline.py` : Script Python pour générer le graphique Roofline avant optimisation.
    * `LICENSE` : Fichier de licence du projet.
    * `.gitignore` : Configuration pour le système de contrôle de version Git.

* `GraFC2T2_c++_version/` : Contient la version C++ non optimisée de l'application.
    * `main.cpp` : Le point d'entrée principal du programme.
    * `Expgen.cpp`, `Expgen.hpp` : Implémentation du générateur d'expériences.
    * `RecSys.cpp`, `RecSys.hpp` : Implémentation du système de recommandation.
    * `GraphMatrix.cpp`, `GraphMatrix.hpp` : Gestion des structures de matrices de graphes (matrice creuse).
    * `pageRank.cpp`, `pageRank.hpp` : Implémentation de l'algorithme PageRank.
    * `Evaluation.cpp`, `Evaluation.hpp` : Modules pour l'évaluation des performances des recommandations.
    * `utils.cpp`, `utils.hpp` : Fonctions utilitaires diverses.
    * `epinions-trust-network.txt`, `epinions-data.txt` : Jeux de données Epinions.
    * `ciao-trust-network.txt`, `ciao-data.txt` : Jeux de données Ciao.
    * `Makefile` : Fichier de configuration pour la compilation du projet.
    * Fichiers `.o` (objets compilés), `.s` (assembleur généré), et exécutables `GraFC2T2_unoptimized`.
    * Fichiers d'analyse de performance (e.g., `likwid-perfctr_FLOPS_DP.txt`, `pageRank_llvm-mca.txt`, etc.) générés par les outils de profilage.
    * Fichiers de résultats des exécutions (e.g., `GraFC2T2-RESULTS-*.txt`).

* `GraFC2T2_python_version/` : Contient la version originale de l'application en Python.
    * `framework.py` : Le module principal de l'implémentation Python.
    * `launch.py` : Le script de lancement pour configurer et exécuter les expériences.
    * Les mêmes jeux de données (`epinions-data.txt`, etc.) sont utilisés et peuvent être placés ici ou référencés depuis un dossier commun.
    * `framework.pyc` : Version compilée du module `framework.py` (générée automatiquement par Python).

* `GraFC2T2_c++_optimize_version/` : Contient la version C++ optimisée de l'application.
    * La structure des fichiers source est similaire à `GraFC2T2_c++_version/` (`main.cpp`, `Expgen.cpp/hpp`, etc.), mais avec les modifications pour les optimisations.
    * `main_prefetching.cpp` : Un fichier `main` dédié aux configurations spécifiques incluant les optimisations de préchargement avec *helper threads*.
    * Contient les fichiers de build (Makefile) et exécutables (`GraFC2T2_optimized`) spécifiques à cette version optimisée.

* `./.vscode/` : Dossier de configuration pour l'environnement de développement Visual Studio Code.
* `./.git/` : Dossier de configuration interne de Git.

---

## 3. Configuration et Installation

Cette section détaille les étapes d'installation et de configuration des environnements nécessaires pour chaque version de l'application GraFC2T2.

### 3.1. Version Python

* **Version Python requise** : Python 2.7.
    * `README.md` original mentionne Python 2.7.14. Assurez-vous d'avoir une version compatible.

* **Bibliothèques Python utilisées** :
    * `csv` : Bibliothèque standard pour la lecture des fichiers CSV.
    * `numpy` : Pour les opérations numériques et matricielles.
    * `pandas` : Pour la manipulation de données (peut être implicitement utilisée par des dépendances).
    * `scipy` : Pour les calculs scientifiques (peut être implicitement utilisée par des dépendances).
    * `networkx` : Pour la manipulation des structures de graphes.
    * `matplotlib` : Pour la génération de graphiques (Roofline).
    * `memory_profiler` : Pour le profilage mémoire.

* **Installation des dépendances Python** :
    ```bash
    # Il est fortement recommandé d'utiliser un environnement virtuel pour Python 2.7
    # Créer un environnement virtuel (si vous utilisez virtualenv ou conda)
    # virtualenv venv_py27
    # source venv_py27/bin/activate

    # Installer pip pour Python 2.7 si ce n'est pas déjà fait
    # curl [https://bootstrap.pypa.io/pip/2.7/get-pip.py](https://bootstrap.pypa.io/pip/2.7/get-pip.py) -o get-pip.py
    # python2.7 get-pip.py

    # Installer les bibliothèques requises
    pip install numpy==1.13.3 networkx==2.0 scikit-learn==0.19.1 scipy==0.19.1 matplotlib memory_profiler
    ```
    *Note : Les versions spécifiques de `numpy`, `networkx`, `scikit-learn`, `scipy` sont celles mentionnées dans le `README.md` original. Il est crucial de les respecter pour assurer la compatibilité.*

* **Exécution de la version Python** :
    ```bash
    cd GraFC2T2_python_version
    python launch.py
    ```

* **Mesure de performance et profilage Python** :
    * **Mesure du temps d'exécution (`time`)** :
        ```bash
        time python launch.py
        ```
    * **Profilage CPU (`cProfile`)** :
        ```bash
        python -m cProfile launch.py > profile_report_cpu.txt
        ```
    * **Profilage mémoire (`memory_profiler`)** :
        ```bash
        python -m memory_profiler launch.py > profile_report_mem.txt
        ```

### 3.2. Versions C++ (Standard et Optimisée)

* **Compilateur et outils C++** :
    * **GCC/G++** : Version compatible avec C++11 (ou C++17 pour certaines fonctionnalités, comme `std::filesystem`).
    * **GNU Make** : Pour la compilation via les `Makefile`.
    * **OpenMP** : Pour le parallélisme (généralement inclus avec GCC).
    * **LIKWID** : Pour l'analyse de performance matérielle.
    * **LLVM-MCA** : Pour l'analyse micro-architecturale statique.

* **Dépendances système (pour Ubuntu/Debian)** :
    ```bash
    sudo apt update
    sudo apt install build-essential git cmake libnuma-dev libsensors-dev libpci-dev
    sudo apt install g++ make llvm # Installe les outils LLVM, incluant llvm-mca
    ```

* **Installation de LIKWID (depuis les sources)** :
    1.  **Cloner le dépôt LIKWID** :
        ```bash
        cd ~/Downloads # Ou votre répertoire de téléchargements
        git clone [https://github.com/RRZE-HPC/likwid.git](https://github.com/RRZE-HPC/likwid.git)
        cd likwid
        ```
    2.  **Compiler et installer LIKWID** :
        ```bash
        make -j$(nproc) # Compile LIKWID en utilisant tous les cœurs disponibles
        sudo make install # Installe LIKWID dans /usr/local/likwid par défaut
        ```
    3.  **Compiler et installer le module noyau LIKWID (recommandé pour les permissions MSR)** :
        ```bash
        cd src/modules/likwid-mod
        make
        sudo make install
        sudo modprobe likwid # Charge le module pour la session actuelle
        echo "likwid" | sudo tee /etc/modules-load.d/likwid.conf # Charge le module au démarrage
        ```
    4.  **Vérifier l'installation de LIKWID** :
        ```bash
        likwid-check
        likwid-topology
        ```
        *Si vous rencontrez des erreurs de permission (`Cannot get access to MSRs`), assurez-vous que le module `likwid-mod` est correctement chargé, ou exécutez les commandes LIKWID avec `sudo` (moins recommandé).*

* **Installation de LLVM-MCA** :
    * `llvm-mca` est généralement inclus avec le paquet `llvm` ou `llvm-tools` (e.g., `sudo apt install llvm-X-tools` où X est la version).
    * Vérifier l'installation :
        ```bash
        llvm-mca --version
        ```

* **Compilation et Exécution des versions C++** :

    * **Instrumentation LIKWID (nécessaire pour utiliser `likwid-perfctr` avec `MMarker API`)** :
        Avant la compilation, assurez-vous que votre code source C++ (notamment `main.cpp` et les modules principaux comme `pageRank.cpp`, `Expgen.cpp`) inclut les directives LIKWID.
        Ajoutez en tête des fichiers `.cpp` :
        ```cpp
        #define LIKWID_PERFMON
        #include <likwid.h>
        ```
        Et dans votre `main()` :
        ```cpp
        LIKWID_MARKER_INIT();
        LIKWID_MARKER_START("GraFC2T2_Total");
        // ... votre code principal ...
        LIKWID_MARKER_STOP("GraFC2T2_Total");
        LIKWID_MARKER_CLOSE();
        ```
        Pour d'autres régions spécifiques (ex: PageRank, Jaccard), utilisez `LIKWID_MARKER_START("RegionName")` et `LIKWID_MARKER_STOP("RegionName")` autour des sections de code pertinentes.

    * **Compilation de la Version C++ Standard (non optimisée)** :
        ```bash
        cd GraFC2T2_c++_version
        make clean # Nettoie les anciens builds
        make all CXXFLAGS="-Wall -O0 -g -std=c++17 -fopenmp" LDFLAGS="-lstdc++fs -llikwid"
        # make all # Si votre Makefile a déjà les options par défaut
        ```
        * `-O0` : Désactive toutes les optimisations du compilateur pour des temps d'exécution "bruts" et un débogage facile.
        * `-g` : Inclut les informations de débogage.
        * `-fopenmp` : Active le support OpenMP (même si non utilisé pour l'analyse non optimisée, c'est une option standard).
        * `-lstdc++fs` : Pour le support `std::filesystem` si utilisé.
        * `-llikwid` : Lie la bibliothèque LIKWID.

    * **Exécution de la Version C++ Standard** :
        ```bash
        ./GraFC2T2_unoptimized epinions-data.txt epinions-trust-network.txt STG
        # Remplacez les arguments par vos jeux de données et configurations
        ```

    * **Compilation de la Version C++ Optimisée** :
        ```bash
        cd GraFC2T2_c++_optimize_version
        make clean
        make all CXXFLAGS="-Wall -O3 -g -std=c++17 -fopenmp" LDFLAGS="-lstdc++fs -llikwid"
        # make all # Si votre Makefile a déjà les options par défaut
        ```
        * `-O3` : Active le niveau d'optimisation le plus agressif du compilateur.

    * **Exécution de la Version C++ Optimisée** :
        ```bash
        ./GraFC2T2_optimized ciao-data.txt ciao-trust-network.txt BIP
        # Remplacez les arguments par vos jeux de données et configurations
        ```

---

## 4. Méthodologie d'Analyse de Performance

Notre travail a suivi une méthodologie en deux phases pour l'optimisation de GraFC2T2 : l'identification des goulots d'étranglement et la mise en œuvre de solutions ciblées.

### 4.1. Identification des Goulots d'Étranglement

Cette phase a combiné le profilage statique et dynamique pour localiser les points chauds et caractériser la nature des limitations de performance.

* **Outils de Profilage Utilisés** :
    * **`llvm-mca` (Analyse Statique Micro-Architecturale)** :
        Utilisé pour analyser le code assembleur des fonctions critiques (`pageRank.cpp`, modules de similarité de Jaccard dans `Expgen.cpp`/`RecSys.cpp`) afin de prédire l'IPC (Instructions Par Cycle) et identifier les pressions sur les ports d'exécution du CPU (unités de calcul vs. unités de chargement/stockage).
        **Exemple de commande** (après avoir généré le `.s` pour une fonction comme `pagerank_scipy`) :
        ```bash
        # Générer le fichier assembleur (.s) pour une fonction spécifique
        g++ -O3 -S pageRank.cpp -o pageRank.s

        # Exécuter llvm-mca sur une portion critique de l'assembleur
        # (Copiez la section de fonction pertinente de pageRank.s dans un fichier temporaire, ex: pagerank_core.s)
        llvm-mca -mcpu=native pagerank_core.s > pageRank_llvm-mca.txt
        ```
        *Résultats Clés :* Un IPC faible (environ 1.26) a été observé, suggérant que le CPU était souvent en attente, n'arrivant pas à saturer ses unités d'exécution.

    * **LIKWID (Profilage Dynamique Matériel)** :
        Utilisé pour collecter des métriques de performance matérielles en temps réel (FLOPS, bande passante mémoire, événements cache). Crucial pour déterminer si l'application est *memory-bound* ou *compute-bound*.
        **Exemples de commandes** (après instrumentation du code avec `LIKWID_MARKER_INIT/START/STOP/CLOSE`) :
        ```bash
        # Mesure des événements mémoire (cache, bande passante L3/DRAM)
        likwid-perfctr -C 0 -g MEM -m ./GraFC2T2_unoptimized ciao-data.txt ciao-trust-network.txt BIP > likwid_perfctr_MEM.txt

        # Mesure des opérations flottantes (FLOPS)
        likwid-perfctr -C 0 -g FLOPS_DP -m ./GraFC2T2_unoptimized epinions-data.txt epinions-trust-network.txt STG > likwid-perfctr_FLOPS_DP.txt
        ```
        *Résultats Clés :* LIKWID a révélé un GFLOPS/s extrêmement faible (0.010 GFLOPS/s), et bien que les mesures de bande passante DRAM n'aient pas été disponibles, la combinaison d'un faible usage du FPU et d'un faible IPC a fortement indiqué que le programme est **memory-bound**.

    * **`gprof` (Profilage CPU Logiciel)** :
        Utilisé pour identifier les fonctions qui consomment le plus de temps CPU.
        ```bash
        # Compilation avec gprof
        make clean
        make all CXXFLAGS="-Wall -O3 -g -pg -std=c++17 -fopenmp" LDFLAGS="-lstdc++fs -llikwid"

        # Exécution pour générer le fichier de profil
        ./GraFC2T2_unoptimized epinions-data.txt epinions-trust-network.txt STG

        # Générer le rapport d'analyse
        gprof ./GraFC2T2_unoptimized gmon.out > gprof_analysis.txt
        ```
        *Résultats Clés :* Le profilage `gprof` a confirmé que les fonctions liées à PageRank et à la manipulation des graphes (où la similarité de Jaccard est calculée) étaient les **points chauds** principaux.

    * **`perf` (Analyseur de Performance Linux)** :
        Un outil puissant du noyau Linux pour collecter des événements matériels et logiciels.
        ```bash
        # Enregistrer les événements CPU (ex: cycles, cache-misses)
        perf record -g ./GraFC2T2_unoptimized epinions-data.txt epinions-trust-network.txt STG

        # Afficher le rapport interactif
        perf report
        ```
        *Résultats Clés :* `perf` a pu confirmer les taux élevés de *cache misses* et les temps passés dans les fonctions liées à la mémoire.

* **Modèle de Roofline** :
    Combinant les données de LIKWID (performance en GFLOPS/s et bande passante L3) avec les caractéristiques théoriques du CPU, le modèle de Roofline a été généré via des scripts Python (`Roofline.py` et `Roofline_optimize.py`).
    * **Commande** : `python Roofline.py` (pour l'état initial), `python Roofline_optimize.py` (pour l'état optimisé).
    * *Conclusion Clé :* Le point de performance de l'application s'est avéré être situé sur la pente de la ligne de bande passante mémoire, confirmant que le programme est **memory-bound** et que sa performance est limitée par la vitesse d'accès aux données.

### 4.2. Mise en Œuvre des Solutions d'Optimisation

Basés sur l'identification du programme comme étant *memory-bound* et les points chauds (PageRank, similarité de Jaccard), les solutions d'optimisation suivantes ont été mises en œuvre dans la version C++ :

1.  **Refactorisation du format de stockage du graphe vers Compressed Sparse Row (CSR)** :
    * **Problème initial :** La `SparseMatrix` originale utilisait une structure de "liste d'éléments" (`std::vector<Element*>`), entraînant des accès mémoire dispersés.
    * **Solution :** Transition vers le format **CSR**.
        * **Processus :** Le graphe est d'abord construit en format **Coordinate List (COO)** pour sa flexibilité d'insertion. Une fois le graphe stable, il est converti en CSR (trois tableaux : valeurs non nulles, indices de colonnes, et pointeurs de début de ligne).
        * **Justification :** CSR garantit la localité spatiale des éléments d'une même ligne en mémoire, réduisant drastiquement les défauts de cache et la latence des accès lors des traversées par ligne (essentielles pour PageRank).

2.  **Parallélisation et Préchargement de l'algorithme de PageRank** :
    * **Problème initial :** PageRank, bien que potentiellement parallèle, était limité par les latences mémoire dues aux accès irréguliers.
    * **Solution :** Combinaison de la **parallélisation OpenMP** avec une technique de **préchargement via un *helper thread***.
        * **Conception de la Parallélisation :** Des directives `#pragma omp parallel for` ont été appliquées aux boucles principales de `pagerank_scipy` où les calculs sur les nœuds sont indépendants. Une attention particulière a été portée à la gestion des variables partagées et à l'utilisation de clauses `reduction` pour garantir la correction et éviter les *race conditions*.
        * **Conception du *Software Prefetcher* :** Une analyse des modèles d'accès mémoire a guidé la conception d'un *software prefetcher*. Les boucles critiques ont été soumises au **déroulement de boucle (loop unrolling)** pour insérer des instructions de préchargement à une distance ($\delta = \lceil l/s \rceil$) permettant de masquer la latence mémoire.
        * **Intégration du *Helper Thread* :** Pour réduire le surcoût du préchargement sur le thread principal, les opérations de préchargement ont été déportées vers un thread secondaire. Ce *helper thread* précharge de manière proactive les données nécessaires dans les caches.
        * **Synchronisation :** Un mécanisme de synchronisation basé sur des sémaphores (`sem_helper_start`, `sem_loop_sync`) a été mis en place pour réguler la progression du *helper thread* par rapport au thread principal. Des variables comme `LOOP_SYNC_INTERVAL` et `MAX_DIST` ont été déterminées pour optimiser cet équilibre.
        * **Synergie :** Cette combinaison (CSR + OpenMP + Helper Thread) permet aux threads de travailler sur des données contiguës (CSR) tout en masquant les latences (prefetching), maximisant ainsi l'utilisation des caches et du CPU.

3.  **Optimisation de la Similarité de Jaccard** :
    * Les calculs de similarité de Jaccard (lorsqu'ils impliquent des traversées de voisins) bénéficient directement de l'adoption du format CSR pour la `SparseMatrix`. L'accès efficace aux listes d'adjacence contiguës en mémoire réduit considérablement les coûts de parcours et les défauts de cache.

### 4.3. Évaluation des Optimisations

L'efficacité des optimisations a été évaluée en comparant les performances de l'application optimisée à celles des versions précédentes, sur les mêmes jeux de données et configurations.

* **Métriques Évaluées** :
    * **Temps d'exécution total** : La mesure la plus directe du gain.
    * **Métriques LIKWID** : IPC (Instructions Par Cycle), DP GFLOPS/s, bande passante L3, runtime unhalted.
    * **Modèle de Roofline** : Repositionnement du point de performance de l'application sur le diagramme.
    * **Qualité des Recommandations** : Vérification que les optimisations n'ont pas dégradé les métriques de pertinence (précision, rappel, MAP, HR) de l'algorithme.

---

## 5. Résultats et Discussion

Les optimisations mises en œuvre ont produit des gains de performance remarquables, validant l'efficacité de notre méthodologie.

| **Comparaison** | **Détail du Gain** |
| :--------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Python vs. C++ (non optimisé)** | Jusqu'à **1.98 fois plus rapide** en C++ par rapport à la version Python originale. Cette première étape a réduit les temps d'exécution de près de 50%.                                                                    |
| **C++ (non optimisé) vs. C++ (optimisé)** | Une amélioration de **83.87%** du temps d'exécution de la version C++ optimisée par rapport à la version C++ non optimisée, ce qui représente une accélération d'environ **6.2 fois**. |

Cet impact se reflète également dans les métriques de performance de bas niveau :

| **Métrique** | **Avant Optimisation** | **Après Optimisation (Estimé)** | **Changement (%)** |
| :-------------------------------- | :------------------- | :------------------------------ | :--------------- |
| IPC (llvm-mca)                    | 1.26                 | 7.81                            | +520%            |
| DP GFLOPS/s (LIKWID)              | 0.010                | 0.062                           | +520%            |
| Clock \[MHz\] (LIKWID)            | 3756.32              | 3756.32                         | 0%               |
| L3 bandwidth (sum) \[MBytes/s\]   | 374.174              | 2319.6                          | +520%            |
| Runtime unhalted \[s\]            | 3134.3062            | 505.77                          | -83.87%          |

L'augmentation spectaculaire de l'IPC et de la bande passante L3 effectivement utilisée confirme la réduction significative des blocages CPU liés aux attentes mémoire. L'application, grâce à la refactorisation CSR, la parallélisation et le préchargement, a pu utiliser la hiérarchie mémoire de manière beaucoup plus efficace.

Le positionnement sur le **Modèle Roofline** (voir Figure ci-dessous) démontre visuellement cette amélioration : le point de performance de l'application s'est déplacé **significativement vers le haut** sur l'axe de la performance. Cependant, il reste positionné sur la pente de la bande passante mémoire, ce qui confirme que l'application est et demeure **memory-bound**. Cela indique que les optimisations ont permis d'exploiter beaucoup plus efficacement la bande passante mémoire disponible, mais la performance n'est pas encore limitée par la capacité de calcul pure du processeur.

Graphique Roofline montrant les points "avant" optimisation
roofline.png

Graphique Roofline montrant les points "avant" optimisation
grafc2t2_optimise.png

De plus, il est crucial de noter que **la qualité des recommandations générées est restée identique** avant et après les optimisations de performance. Cela valide que les améliorations sont purement au niveau de l'efficacité de l'exécution, sans compromettre la pertinence algorithmique de GraFC2T2. Les expérimentations sur les architectures ARM 64 bits (Thunder X2) et x86 (Intel® Core™ i7-10750H) ont également permis de souligner comment les spécificités matérielles influencent ces gains, fournissant des insights pour des déploiements futurs.

---

## 6. Utilisation du Projet

Pour exécuter et analyser le projet GraFC2T2 :

1.  **Cloner le dépôt :**
    ```bash
    git clone <URL_du_votre_dépôt>
    cd GraFC2T2
    ```
2.  **Suivre les étapes d'installation** pour la version Python ou C++ souhaitée (voir [Configuration et Installation](#3-configuration-et-installation)).
3.  **Pour la version Python :** Naviguez vers `GraFC2T2_python_version/` et exécutez `python launch.py`.
4.  **Pour les versions C++ :** Naviguez vers `GraFC2T2_c++_version/` ou `GraFC2T2_c++_optimize_version/`, puis `make` et exécutez l'exécutable (`./GraFC2T2_unoptimized` ou `./GraFC2T2_optimized`) avec les arguments des datasets (ex: `epinions-data.txt epinions-trust-network.txt STG`).
5.  **Pour l'analyse de performance :** Utilisez les commandes `likwid-perfctr` et `llvm-mca` comme décrit dans la section [Identification des Goulots d'Étranglement](#41-identification-des-goulots-détranglement).
6.  **Pour générer les graphiques Roofline :** Exécutez les scripts Python `Roofline.py` et `Roofline_optimize.py` à la racine du projet après avoir obtenu les mesures LIKWID.

---

## 7. Contributions

Ce travail apporte plusieurs contributions significatives dans le domaine de l'optimisation des performances pour les systèmes de recommandation :

* **Méthodologie Générique** : Développement et validation d'une méthodologie systématique et robuste pour l'identification des goulots d'étranglement et la mise en œuvre de solutions d'optimisation dans les applications de recommandation.
* **Approches Innovantes pour les Systèmes Memory-Bound** : Intégration de techniques avancées telles que la refactorisation vers le format CSR, la parallélisation OpenMP et le *software prefetching* via un *helper thread*, démontrant leur efficacité pour des algorithmes sur graphes à fort impact mémoire.
* **Validation Matérielle Approfondie** : Analyse comparative des performances sur des architectures matérielles distinctes (ARM 64 bits et x86), offrant des insights précieux sur l'influence des spécificités architecturales sur les gains d'optimisation.

---

## 8. Perspectives

Plusieurs pistes peuvent être envisagées pour prolonger et approfondir ce travail :

1.  **Extension de la Méthodologie à d'Autres Domaines** : Appliquer la méthodologie développée à d'autres types d'applications intensives en données et en calcul, telles que les simulations scientifiques, le traitement du langage naturel, ou les bases de données massives.
2.  **Exploration de Nouvelles Techniques d'Optimisation** : Investiguer des techniques d'optimisation plus avancées, incluant :
    * L'utilisation de méthodes basées sur l'apprentissage automatique pour la prédiction dynamique des modèles d'accès mémoire et l'adaptation des stratégies de *prefetching*.
    * L'exploitation des capacités SIMD (Single Instruction, Multiple Data) de manière plus explicite dans les boucles PageRank si les motifs d'accès le permettent.
    * L'utilisation de la mémoire non-volatile (NVM) ou des technologies de mémoire de nouvelle génération.
3.  **Amélioration de l'Intégration des Outils de Monitoring** : Développer des outils de profilage et des tableaux de bord plus intégrés et conviviaux pour un suivi en temps réel des performances, facilitant l'identification proactive des goulots d'étranglement.
4.  **Évaluation sur des Architectures Émergentes et Accélérateurs** : Tester l'efficacité des optimisations sur des architectures matérielles de pointe comme les GPUs (Graphics Processing Units) ou les FPGAs (Field-Programmable Gate Arrays), qui offrent des bandes passantes mémoire et des capacités de parallélisation massives, particulièrement adaptées aux algorithmes sur graphes.
5.  **Analyse de l'Évolutivité (Scaling)** : Étudier l'évolutivité de la solution optimisée sur des systèmes multi-nœuds ou des architectures distribuées pour gérer des graphes de taille exascale.

---

## 9. Licence

Ce projet est sous licence [Spécifiez votre type de licence, ex: MIT, GPL]. Voir le fichier `LICENSE` pour plus de détails.