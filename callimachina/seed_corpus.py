#!/usr/bin/env python3
"""
Seed the CALLIMACHINA database with 400+ classical works for scale-up
"""

import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import db


def seed_database(target_count: int = 400):
    """Seed the database with classical works."""
    
    print("🏛️" + "="*70)
    print(f"SEEDING CALLIMACHINA DATABASE WITH {target_count} CLASSICAL WORKS")
    print("="*70 + "🏛️")
    print()
    
    # Classical works corpus - organized by genre
    classical_corpus = [
        # PHILOSOPHY (80 works)
        # Presocratics
        ("Thales", "OnNature", "philosophy"), ("Anaximander", "OnNature", "philosophy"),
        ("Anaximenes", "OnNature", "philosophy"), ("Pythagoras", "SacredDiscourse", "philosophy"),
        ("Heraclitus", "OnNature", "philosophy"), ("Parmenides", "OnNature", "philosophy"),
        ("Anaxagoras", "OnNature", "philosophy"), ("Empedocles", "OnNature", "philosophy"),
        ("Zeno", "Paradoxes", "philosophy"), ("Melissus", "OnNature", "philosophy"),
        ("Leucippus", "OnMind", "philosophy"), ("Democritus", "Cosmology", "philosophy"),
        ("Protagoras", "Truth", "philosophy"), ("Gorgias", "OnNonExistence", "philosophy"),
        ("Prodicus", "OnNature", "philosophy"), ("Thrasymachus", "OnJustice", "philosophy"),
        ("Hippias", "OlympicDiscourse", "philosophy"), ("Critias", "Sisyphus", "philosophy"),
        ("Alcmaeon", "OnNature", "philosophy"), ("Pherecydes", "SevenRecesses", "philosophy"),
        
        # Socratic circle
        ("Socrates", "Dialogues", "philosophy"), ("Antisthenes", "Ajax", "philosophy"),
        ("Aristippus", "OnEducation", "philosophy"), ("Euclid", "SocraticDialogues", "philosophy"),
        ("Phaedo", "Zopyrus", "philosophy"), ("Simon", "OnJustice", "philosophy"),
        ("Cebes", "Pinax", "philosophy"), ("Glaucon", "OnTheJust", "philosophy"),
        ("Simmias", "OnTheSoul", "philosophy"), ("Crito", "Dialogues", "philosophy"),
        
        # Plato's lost works
        ("Plato", "OnTheGood", "philosophy"), ("Plato", "HippiasMajor", "philosophy"),
        ("Plato", "HippiasMinor", "philosophy"), ("Plato", "GreaterHippias", "philosophy"),
        ("Plato", "LesserHippias", "philosophy"), ("Plato", "Meno", "philosophy"),
        ("Plato", "Cratylus", "philosophy"), ("Plato", "Euthydemus", "philosophy"),
        ("Plato", "Symposium", "philosophy"), ("Plato", "Phaedo", "philosophy"),
        ("Plato", "Parmenides", "philosophy"), ("Plato", "Theaetetus", "philosophy"),
        ("Plato", "Sophist", "philosophy"), ("Plato", "Statesman", "philosophy"),
        ("Plato", "Philebus", "philosophy"), ("Plato", "Timaeus", "philosophy"),
        ("Plato", "Critias", "philosophy"), ("Plato", "Laws", "philosophy"),
        
        # Aristotelian lost works
        ("Aristotle", "OnPhilosophy", "philosophy"), ("Aristotle", "OnMotion", "philosophy"),
        ("Aristotle", "Protrepticus", "philosophy"), ("Aristotle", "OnIdeas", "philosophy"),
        ("Aristotle", "OnTheGood", "philosophy"), ("Aristotle", "Eudemus", "philosophy"),
        ("Aristotle", "OnPrayer", "philosophy"), ("Aristotle", "OnEducation", "philosophy"),
        ("Aristotle", "OnWealth", "philosophy"), ("Aristotle", "OnPleasure", "philosophy"),
        
        # Peripatetic school
        ("Theophrastus", "OnDiscoveries", "philosophy"), ("Theophrastus", "OnMotion", "philosophy"),
        ("Theophrastus", "Metaphysics", "philosophy"), ("Theophrastus", "OnTheSoul", "philosophy"),
        ("Theophrastus", "OnSenses", "philosophy"), ("Theophrastus", "Characters", "philosophy"),
        ("Eudemus", "HistoryOfTheology", "philosophy"), ("Eudemus", "HistoryOfPhilosophy", "philosophy"),
        ("Strato", "OnVoid", "philosophy"), ("Strato", "OnTheSoul", "philosophy"),
        ("Lyco", "OnTheSoul", "philosophy"), ("Aristoxenus", "ElementsOfHarmony", "philosophy"),
        ("Dicaearchus", "OnTheSoul", "philosophy"), ("Dicaearchus", "Lives", "philosophy"),
        
        # Stoics
        ("Zeno", "Republic", "philosophy"), ("Zeno", "OnNature", "philosophy"),
        ("Cleanthes", "HymnToZeus", "philosophy"), ("Cleanthes", "OnNature", "philosophy"),
        ("Chrysippus", "OnNature", "philosophy"), ("Chrysippus", "OnLogic", "philosophy"),
        ("Chrysippus", "OnEthics", "philosophy"), ("Chrysippus", "OnPhysics", "philosophy"),
        ("Persaeus", "Logic", "philosophy"), ("Persaeus", "Ethics", "philosophy"),
        ("Sphaerus", "OnTheSoul", "philosophy"), ("Sphaerus", "OnNature", "philosophy"),
        ("Boethus", "OnNature", "philosophy"), ("Panaetius", "OnDuty", "philosophy"),
        ("Posidonius", "OnGods", "philosophy"), ("Posidonius", "OnTheSoul", "philosophy"),
        
        # Epicureans
        ("Epicurus", "OnNature", "philosophy"), ("Epicurus", "OnGods", "philosophy"),
        ("Epicurus", "OnVision", "philosophy"), ("Epicurus", "OnJustice", "philosophy"),
        ("Metrodorus", "OnWealth", "philosophy"), ("Metrodorus", "OnNobleBirth", "philosophy"),
        ("Hermarchus", "OnJustice", "philosophy"), ("Polyaenus", "OnPhilosophy", "philosophy"),
        ("Colotes", "OnPlato", "philosophy"), ("Colotes", "OnPerception", "philosophy"),
        
        # Skeptics
        ("Pyrrho", "OnPhilosophy", "philosophy"), ("Timon", "Silloi", "philosophy"),
        ("Aenesidemus", "PyrrhonianDiscourses", "philosophy"), ("Agrippa", "FiveModes", "philosophy"),
        ("Sextus", "OutlinesOfPyrrhonism", "philosophy"), ("Sextus", "AgainstTheLogicians", "philosophy"),
        ("Sextus", "AgainstThePhysicists", "philosophy"), ("Sextus", "AgainstTheEthicists", "philosophy"),
        
        # Hellenistic-Roman
        ("Cicero", "Hortensius", "philosophy"), ("Cicero", "Consolatio", "philosophy"),
        ("Cicero", "Academica", "philosophy"), ("Cicero", "DeFinibus", "philosophy"),
        ("Cicero", "TusculanDisputations", "philosophy"), ("Cicero", "DeNaturaDeorum", "philosophy"),
        ("Seneca", "Dialogues", "philosophy"), ("Seneca", "Letters", "philosophy"),
        ("Seneca", "NaturalesQuaestiones", "philosophy"), ("Seneca", "DeClementia", "philosophy"),
        ("Epictetus", "Discourses", "philosophy"), ("Epictetus", "Enchiridion", "philosophy"),
        ("MarcusAurelius", "Meditations", "philosophy"), ("MarcusAurelius", "Letters", "philosophy"),
        
        # MATHEMATICS & SCIENCE (80 works)
        # Pre-Socratic science
        ("Thales", "Astronomy", "science"), ("Anaximander", "MapOfWorld", "science"),
        ("Pythagoras", "Mathematics", "science"), ("Philolaus", "Cosmology", "science"),
        ("Alcmaeon", "MedicalTheory", "science"), ("Empedocles", "OnNature", "science"),
        ("Anaxagoras", "Astronomy", "science"), ("Democritus", "Cosmology", "science"),
        ("Oenopides", "Astronomy", "science"), ("Hippocrates", "Astronomy", "science"),
        
        # Classical mathematics
        ("Hippocrates", "Elements", "science"), ("Hippocrates", "QuadratureOfLunes", "science"),
        ("Hippias", "Quadratrix", "science"), ("Archytas", "Geometry", "science"),
        ("Theaetetus", "PlatonicSolids", "science"), ("Eudoxus", "Phaenomena", "science"),
        ("Eudoxus", "Mirror", "science"), ("Eudoxus", "OnSpeeds", "science"),
        ("Menaechmus", "ConicSections", "science"), ("Menaechmus", "Geometry", "science"),
        ("Deinostratus", "Quadratrix", "science"), ("Autolycus", "OnTheMovingSphere", "science"),
        
        # Hellenistic mathematics
        ("Euclid", "Elements", "science"), ("Euclid", "Data", "science"),
        ("Euclid", "OnDivisions", "science"), ("Euclid", "Phaenomena", "science"),
        ("Euclid", "Optics", "science"), ("Euclid", "Catoptrics", "science"),
        ("Archimedes", "OnTheSphereAndCylinder", "science"), ("Archimedes", "OnConoidsAndSpheroids", "science"),
        ("Archimedes", "OnSpirals", "science"), ("Archimedes", "OnEquilibriumOfPlanes", "science"),
        ("Archimedes", "TheSandReckoner", "science"), ("Archimedes", "QuadratureOfParabola", "science"),
        ("Archimedes", "OnFloatingBodies", "science"), ("Archimedes", "Ostomachion", "science"),
        ("Apollonius", "Conics", "science"), ("Apollonius", "OnTangencies", "science"),
        ("Apollonius", "CuttingOffOfRatio", "science"), ("Apollonius", "CuttingOffOfArea", "science"),
        ("Apollonius", "Inclinations", "science"), ("Apollonius", "PlaneLoci", "science"),
        ("Nicomedes", "OnConchoids", "science"), ("Diocles", "OnBurningMirrors", "science"),
        ("Perseus", "OnSpiricSections", "science"), ("Hipparchus", "OnSizesAndDistances", "science"),
        ("Hipparchus", "OnTheLengthOfYear", "science"), ("Hipparchus", "Geography", "science"),
        ("Posidonius", "Geography", "science"), ("Posidonius", "Meteorology", "science"),
        ("Geminus", "Phaenomena", "science"), ("Geminus", "Mathematics", "science"),
        ("Theodosius", "Spherics", "science"), ("Theodosius", "OnHabitations", "science"),
        ("Menelaus", "Spherics", "science"), ("Menelaus", "OnTheTriangle", "science"),
        ("Ptolemy", "Almagest", "science"), ("Ptolemy", "Geography", "science"),
        ("Ptolemy", "Tetrabiblos", "science"), ("Ptolemy", "Optics", "science"),
        ("Ptolemy", "Harmonics", "science"), ("Ptolemy", "PlanetaryHypotheses", "science"),
        ("Pappus", "Collection", "science"), ("Pappus", "CommentaryOnPtolemy", "science"),
        ("Diophantus", "Arithmetica", "science"), ("Diophantus", "OnPolygonalNumbers", "science"),
        ("Anatolius", "OnTheDecad", "science"), ("Serenus", "OnTheSectionOfCylinder", "science"),
        ("Serenus", "OnTheSectionOfCone", "science"), ("Theon", "CommentaryOnAlmagest", "science"),
        ("Hypatia", "CommentaryOnDiophantus", "science"), ("Proclus", "CommentaryOnEuclid", "science"),
        ("Marinus", "CommentaryOnData", "science"), ("Isidore", "Elements", "science"),
        ("Anthemius", "OnBurningMirrors", "science"), ("Eutocius", "CommentaryOnArchimedes", "science"),
        
        # MEDICINE (80 works)
        # Pre-Hippocratic
        ("Pythagoras", "MedicalTheory", "medicine"), ("Alcmaeon", "MedicalTheory", "medicine"),
        ("Democedes", "Medicine", "medicine"), ("Democritus", "MedicalTheory", "medicine"),
        
        # Hippocratic corpus (lost works)
        ("Hippocrates", "OnTheNatureOfMan", "medicine"), ("Hippocrates", "OnTheSacredDisease", "medicine"),
        ("Hippocrates", "Aphorisms", "medicine"), ("Hippocrates", "Epidemics", "medicine"),
        ("Hippocrates", "Prognostics", "medicine"), ("Hippocrates", "OnAncientMedicine", "medicine"),
        ("Hippocrates", "OnAirsWatersPlaces", "medicine"), ("Hippocrates", "OnRegimen", "medicine"),
        ("Hippocrates", "OnSurgery", "medicine"), ("Hippocrates", "OnTheNatureOfBones", "medicine"),
        ("Hippocrates", "OnTheNatureOfMuscles", "medicine"), ("Hippocrates", "OnTheNatureOfVeins", "medicine"),
        ("Hippocrates", "OnTheNatureOfArteries", "medicine"), ("Hippocrates", "OnDiseases", "medicine"),
        ("Hippocrates", "OnDiseasesOfWomen", "medicine"), ("Hippocrates", "OnDiseasesOfGirls", "medicine"),
        
        # 4th century BCE
        ("Diocles", "MedicalWorks", "medicine"), ("Diocles", "OnPleurisy", "medicine"),
        ("Diocles", "OnHemorrhoids", "medicine"), ("Diocles", "OnVision", "medicine"),
        ("Praxagoras", "Medicine", "medicine"), ("Praxagoras", "OnDiseases", "medicine"),
        ("Herophilus", "Anatomy", "medicine"), ("Herophilus", "OnEyes", "medicine"),
        ("Herophilus", "OnThePulse", "medicine"), ("Herophilus", "Midwifery", "medicine"),
        ("Erasistratus", "Medicine", "medicine"), ("Erasistratus", "OnFevers", "medicine"),
        ("Erasistratus", "OnHemorrhage", "medicine"), ("Erasistratus", "OnDiseases", "medicine"),
        
        # 3rd-2nd century BCE
        ("Philinus", "Empiricism", "medicine"), ("Serapion", "Medicine", "medicine"),
        ("Glaucias", "CommentaryOnHippocrates", "medicine"), ("Ctesias", "OnDiseases", "medicine"),
        ("Andreas", "Medicine", "medicine"), ("Aelius", "Medicine", "medicine"),
        ("Eudemus", "Medicine", "medicine"), ("Strato", "OnDiseases", "medicine"),
        
        # 1st century BCE - 1st century CE
        ("Asclepiades", "Medicine", "medicine"), ("Asclepiades", "OnAnatomy", "medicine"),
        ("Themison", "Methodism", "medicine"), ("Themison", "OnDiseases", "medicine"),
        ("Philo", "OnThePulse", "medicine"), ("Philo", "OnDiseases", "medicine"),
        ("Aelius", "OnThePulse", "medicine"), ("Aelius", "OnDiseases", "medicine"),
        
        # 2nd century CE
        ("Aretaeus", "OnCauses", "medicine"), ("Aretaeus", "OnSymptoms", "medicine"),
        ("Aretaeus", "OnCure", "medicine"), ("Aretaeus", "OnChronicDiseases", "medicine"),
        ("Aretaeus", "OnAcuteDiseases", "medicine"), ("Aretaeus", "OnSurgery", "medicine"),
        ("Galen", "OnTheNaturalFaculties", "medicine"), ("Galen", "OnTheElements", "medicine"),
        ("Galen", "OnTemperaments", "medicine"), ("Galen", "OnFaculties", "medicine"),
        ("Galen", "OnTheUseOfParts", "medicine"), ("Galen", "OnTheDoctrines", "medicine"),
        ("Galen", "OnThePulse", "medicine"), ("Galen", "OnDiseases", "medicine"),
        ("Galen", "OnSymptoms", "medicine"), ("Galen", "OnCauses", "medicine"),
        ("Galen", "OnCure", "medicine"), ("Galen", "OnAnatomy", "medicine"),
        ("Galen", "OnHumors", "medicine"), ("Galen", "OnTemperaments", "medicine"),
        
        # Later physicians
        ("Oribasius", "MedicalCollections", "medicine"), ("Oribasius", "Synopsis", "medicine"),
        ("Aetius", "MedicalBooks", "medicine"), ("Aetius", "OnDiseases", "medicine"),
        ("Alexander", "CommentaryOnHippocrates", "medicine"), ("Alexander", "OnThePulse", "medicine"),
        ("Marcellus", "OnDrugs", "medicine"), ("Marcellus", "OnRemedies", "medicine"),
        
        # HISTORY & GEOGRAPHY (80 works)
        # Early logographers
        ("Hecataeus", "Genealogies", "history"), ("Hecataeus", "HistoryOfEgypt", "history"),
        ("Hecataeus", "Periegesis", "history"), ("Hecataeus", "OnAsia", "history"),
        ("Hecataeus", "OnEurope", "history"), ("Hecataeus", "OnLibya", "history"),
        
        # 5th century BCE
        ("Hellanicus", "PriestessesOfHera", "history"), ("Hellanicus", "Phoronis", "history"),
        ("Hellanicus", "Atlantis", "history"), ("Hellanicus", "OnCities", "history"),
        ("Hellanicus", "OnNations", "history"), ("Hellanicus", "OnInventions", "history"),
        ("Acusilaus", "Genealogies", "history"), ("Acusilaus", "HistoryOfArgos", "history"),
        ("Pherecydes", "Histories", "history"), ("Pherecydes", "Genealogies", "history"),
        
        # 4th century BCE
        ("Xanthus", "LydianHistory", "history"), ("Xanthus", "OnLydia", "history"),
        ("Charon", "HistoryOfPersia", "history"), ("Charon", "OnCities", "history"),
        ("Dionysius", "HistoryOfPersia", "history"), ("Dionysius", "OnCities", "history"),
        ("Eudemus", "HistoryOfTheology", "history"), ("Eudemus", "HistoryOfPhilosophy", "history"),
        ("Eudemus", "HistoryOfGeometry", "history"), ("Eudemus", "HistoryOfAstronomy", "history"),
        ("Eudemus", "HistoryOfMedicine", "history"), ("Eudemus", "HistoryOfMagic", "history"),
        
        # Hellenistic historians
        ("Dicaearchus", "LifeOfGreece", "history"), ("Dicaearchus", "OnTheSoul", "history"),
        ("Dicaearchus", "Geography", "history"), ("Dicaearchus", "OnCities", "history"),
        ("Timaeus", "Histories", "history"), ("Timaeus", "OnSicily", "history"),
        ("Timaeus", "OnPyrrhus", "history"), ("Timaeus", "OnAgathocles", "history"),
        ("Polybius", "Histories", "history"), ("Polybius", "OnTactics", "history"),
        ("Polybius", "Geography", "history"), ("Polybius", "OnNumantia", "history"),
        ("Posidonius", "Histories", "history"), ("Posidonius", "OnOcean", "history"),
        ("Posidonius", "Geography", "history"), ("Posidonius", "OnEthics", "history"),
        
        # Geographers
        ("Scylax", "Periplus", "history"), ("Scylax", "OnIndia", "history"),
        ("Hanno", "Periplus", "history"), ("Hanno", "OnLibya", "history"),
        ("Pytheas", "OnOcean", "history"), ("Pytheas", "Geography", "history"),
        ("Eratosthenes", "Geography", "history"), ("Eratosthenes", "OnMeasurement", "history"),
        ("Eratosthenes", "Chronographies", "history"), ("Eratosthenes", "OnComedy", "history"),
        ("Strabo", "Geography", "history"), ("Strabo", "OnHistory", "history"),
        ("Pausanias", "DescriptionOfGreece", "history"), ("Pausanias", "OnAthens", "history"),
        
        # Biographers
        ("Plutarch", "ParallelLives", "history"), ("Plutarch", "Moralia", "history"),
        ("Plutarch", "OnTheSoul", "history"), ("Plutarch", "OnGods", "history"),
        ("Suetonius", "LivesOfTheCaesars", "history"), ("Suetonius", "OnGrammarians", "history"),
        ("Suetonius", "OnRhetoricians", "history"), ("Suetonius", "OnPoets", "history"),
        ("Diogenes", "LivesOfPhilosophers", "history"), ("Diogenes", "OnPoets", "history"),
        
        # POETRY & LITERATURE (80 works)
        # Epic
        ("Homer", "Margites", "poetry"), ("Homer", "Batrachomyomachia", "poetry"),
        ("Homer", "Epigrams", "poetry"), ("Homer", "Hymns", "poetry"),
        ("Hesiod", "CatalogueOfWomen", "poetry"), ("Hesiod", "Astronomy", "poetry"),
        ("Hesiod", "PreceptsOfChiron", "poetry"), ("Hesiod", "Melampodia", "poetry"),
        ("Hesiod", "IdaeanDactyls", "poetry"), ("Hesiod", "DescentOfPeirithous", "poetry"),
        ("Hesiod", "GreatWorks", "poetry"), ("Hesiod", "Aegimius", "poetry"),
        ("Eumelus", "Corinthiaca", "poetry"), ("Eumelus", "ReturnOfTheHeracleidae", "poetry"),
        ("Eumelus", "Prosodion", "poetry"), ("Eumelus", "Processional", "poetry"),
        
        # Lyric poets (archaic)
        ("Archilochus", "Iambi", "poetry"), ("Archilochus", "Elegies", "poetry"),
        ("Sappho", "Odes", "poetry"), ("Sappho", "Epithalamia", "poetry"),
        ("Alcaeus", "Odes", "poetry"), ("Alcaeus", "PoliticalSongs", "poetry"),
        ("Anacreon", "Odes", "poetry"), ("Anacreon", "LovePoems", "poetry"),
        ("Ibycus", "Odes", "poetry"), ("Ibycus", "LovePoems", "poetry"),
        ("Simonides", "Odes", "poetry"), ("Simonides", "Elegies", "poetry"),
        ("Simonides", "Epigrams", "poetry"), ("Simonides", "Scolia", "poetry"),
        ("Stesichorus", "Oresteia", "poetry"), ("Stesichorus", "Helen", "poetry"),
        ("Stesichorus", "Palinode", "poetry"), ("Stesichorus", "Geryoneis", "poetry"),
        ("Alcman", "Partheneia", "poetry"), ("Alcman", "Odes", "poetry"),
        ("Mimnermus", "Nanno", "poetry"), ("Mimnermus", "Smyrneis", "poetry"),
        ("Tyrtaeus", "Elegies", "poetry"), ("Tyrtaeus", "WarSongs", "poetry"),
        ("Callinus", "Elegies", "poetry"), ("Callinus", "WarSongs", "poetry"),
        ("Theognis", "Elegies", "poetry"), ("Theognis", "Advice", "poetry"),
        
        # Lyric poets (classical)
        ("Pindar", "Epinicians", "poetry"), ("Pindar", "Dithyrambs", "poetry"),
        ("Pindar", "Paeans", "poetry"), ("Pindar", "Prosodia", "poetry"),
        ("Pindar", "Partheneia", "poetry"), ("Pindar", "Hyporchemata", "poetry"),
        ("Pindar", "Encomia", "poetry"), ("Pindar", "Threnoi", "poetry"),
        ("Bacchylides", "Epinicians", "poetry"), ("Bacchylides", "Dithyrambs", "poetry"),
        ("Bacchylides", "Paeans", "poetry"), ("Bacchylides", "Encomia", "poetry"),
        ("Corinna", "Odes", "poetry"), ("Corinna", "Epic", "poetry"),
        ("Myrtis", "Odes", "poetry"), ("Myrtis", "Elegies", "poetry"),
        ("Telesilla", "Odes", "poetry"), ("Telesilla", "WarSongs", "poetry"),
        ("Praxilla", "Odes", "poetry"), ("Praxilla", "LovePoems", "poetry"),
        ("Lasus", "Odes", "poetry"), ("Lasus", "Hymns", "poetry"),
        
        # Hellenistic poets
        ("Callimachus", "Aetia", "poetry"), ("Callimachus", "Hymns", "poetry"),
        ("Callimachus", "Epigrams", "poetry"), ("Callimachus", "Iambi", "poetry"),
        ("Callimachus", "Hecale", "poetry"), ("Callimachus", "LockOfBerenice", "poetry"),
        ("Theocritus", "Idylls", "poetry"), ("Theocritus", "Epigrams", "poetry"),
        ("Theocritus", "Hymns", "poetry"), ("Theocritus", "Syrinx", "poetry"),
        ("Apollonius", "Argonautica", "poetry"), ("Apollonius", "Epigrams", "poetry"),
        ("Apollonius", "Foundations", "poetry"), ("Apollonius", "Canopus", "poetry"),
        ("Aratus", "Phaenomena", "poetry"), ("Aratus", "Diosemeia", "poetry"),
        ("Nicander", "Theriaca", "poetry"), ("Nicander", "Alexipharmaca", "poetry"),
        ("Lycophron", "Alexandra", "poetry"), ("Lycophron", "Tragedies", "poetry"),
        ("Euphorion", "Thrax", "poetry"), ("Euphorion", "Hyacinthus", "poetry"),
        ("Euphorion", "Epigrams", "poetry"), ("Euphorion", "Commentary", "poetry"),
        ("Rhianus", "Epigrams", "poetry"), ("Rhianus", "Messeniaca", "poetry"),
        ("Parthenius", "LoveRomances", "poetry"), ("Parthenius", "Epigrams", "poetry"),
        
        # Dramatists (lost plays)
        ("Aeschylus", "Myrmidons", "drama"), ("Aeschylus", "Nereids", "drama"),
        ("Aeschylus", "Phrygians", "drama"), ("Aeschylus", "DaughtersOfTheSun", "drama"),
        ("Aeschylus", "PrometheusUnbound", "drama"), ("Aeschylus", "PrometheusFireBringer", "drama"),
        ("Sophocles", "Triptolemus", "drama"), ("Sophocles", "Niobe", "drama"),
        ("Sophocles", "HelenesGamos", "drama"), ("Sophocles", "Andromeda", "drama"),
        ("Sophocles", "Epeus", "drama"), ("Sophocles", "ReceptionOfZeus", "drama"),
        ("Euripides", "Andromeda", "drama"), ("Euripides", "Hypsipyle", "drama"),
        ("Euripides", "Phaethon", "drama"), ("Euripides", "Cresphontes", "drama"),
        ("Euripides", "Erechtheus", "drama"), ("Euripides", "Oedipus", "drama"),
    ]
    
    print(f"📚 Total works in corpus: {len(classical_corpus)}")
    print(f"🎯 Target for database: {target_count}")
    print()
    
    # Insert works into database
    inserted = 0
    errors = 0
    
    for i, (author, title, genre) in enumerate(classical_corpus[:target_count]):
        try:
            work = {
                'work_id': f"{author}.{title}",
                'author': author,
                'title': title,
                'genre': genre,
                'century': estimate_century(author),
                'status': 'lost',
                'priority_score': round(0.95 - (i * 0.002), 3),  # Gradually decreasing
                'recoverability_score': round(0.8 - (i * 0.001), 3),
                'reconstruction_confidence': None
            }
            
            db.insert_work(work)
            inserted += 1
            
            if (i + 1) % 50 == 0:
                print(f"✅ Inserted {inserted} works...")
                
        except Exception as e:
            errors += 1
            print(f"❌ Error inserting {author}.{title}: {e}")
    
    print()
    print("🏛️" + "="*70)
    print("DATABASE SEEDING COMPLETE")
    print("="*70 + "🏛️")
    print(f"✅ Successfully inserted: {inserted} works")
    print(f"❌ Errors: {errors}")
    print()
    
    # Show database stats
    stats = db.get_reconstruction_stats()
    print("📊 DATABASE STATISTICS:")
    print(f"   Total works: {sum(stats['work_counts'].values())}")
    print(f"   Status breakdown: {stats['work_counts']}")
    print(f"   Top authors: {list(stats['top_authors'].keys())[:5]}")
    print()
    
    # Show sample of inserted works
    works_df = db.get_works_by_priority(limit=10)
    print("🏆 TOP 10 PRIORITY WORKS:")
    print(works_df[['work_id', 'priority_score', 'recoverability_score']].to_string())
    print()
    
    print("🚀 Database ready for large-scale excavation!")
    print()


def estimate_century(author: str) -> int:
    """Estimate century BCE/CE for an author."""
    century_map = {
        # Archaic
        'Homer': -8, 'Hesiod': -7, 'Sappho': -6, 'Alcaeus': -6, 'Alcman': -7,
        'Archilochus': -7, 'Tyrtaeus': -7, 'Callinus': -7, 'Mimnermus': -7,
        'Theognis': -6, 'Pherecydes': -6, 'Hecataeus': -5,
        
        # Classical
        'Aeschylus': -5, 'Sophocles': -5, 'Euripides': -5, 'Aristophanes': -4,
        'Herodotus': -5, 'Thucydides': -4, 'Xenophon': -4, 'Plato': -4,
        'Aristotle': -4, 'Isocrates': -4, 'Demosthenes': -4,
        
        # Hellenistic
        'Theophrastus': -3, 'Euclid': -3, 'Menander': -3, 'Callimachus': -3,
        'Theocritus': -3, 'Apollonius': -3, 'Aratus': -3, 'Archimedes': -2,
        'Eratosthenes': -2, 'Polybius': -2, 'Hipparchus': -1,
        
        # Roman Imperial
        'Ptolemy': 2, 'Galen': 2, 'Athenaeus': 3, 'Diogenes': 3,
        'Pausanias': 2, 'Sextus': 2, 'MarcusAurelius': 2, 'Epictetus': 2,
        
        # Default
        'Unknown': -2
    }
    return century_map.get(author, -2)


if __name__ == '__main__':
    import sys
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    seed_database(target)