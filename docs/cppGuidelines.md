# C++ Programmierrichtlinien
## 1. Motivation und Nutzen

* **Ziel:** Schaffung eines einheitlichen Stils in allen von Sander & Doll-Mitarbeitern erstellten C++-Quelltexten.
* **Vorteile:**
    * Vermeidung fehleranfälliger Konstrukte.
    * Erleichterung des Verständnisses und der Bearbeitung von Code.
    * Minimierung von Reibungsverlusten und Steigerung der Effizienz.

## 2. Anwendungsbereich

* Gilt primär für **neu zu erstellenden Quelltext**.
* Bei **bestehendem Quelltext**: Einzelfallentscheidung, aber langfristig einheitlicher Stil angestrebt.
* **Wichtige Punkte für neuen Code:**
    * Neue Klassenmitglieder müssen den neuen Regeln folgen.
    * Überschreibende virtuelle Funktionen mit `override` kennzeichnen.
    * Neue Funktionen, Typen und Variablen müssen immer einen Dokumentationskommentar erhalten.
    * `NULL` ist durch `nullptr` zu ersetzen.

## 3. Wesentliche Richtlinien

### 3.1. Allgemein

* **Einrückung:** 4 Leerzeichen, keine Tabs.
* **Zeilenlänge:** Max. 135 Zeichen (Ausnahmen möglich).
* **Leerzeichen:** Vor öffnenden Klammern (`(`, `{`, `[`, `<`) ein Leerzeichen, innen keine.
* **Operatoren:** Durch Leerzeichen von Operanden getrennt (Ausnahmen: `::`, `,`, `>`, `>>`, `++`, Komma-Operator).
* Große auskommentierte Codeblöcke entfernen (Versionskontrolle nutzen).

### 3.2. Variablen

* **Namen:** `camelCase`, beginnend mit Kleinbuchstaben (z.B. `variableName`). Einwortige Variablen komplett kleingeschrieben (z.B. `count`).
* Keine ungarische Notation.
* Namen sollen aussagekräftig sein; Abkürzungen nur wenn offensichtlich oder kommentiert.
* Pro Statement nur eine Variablendeklaration.
* **Pointer/Referenzen:** Zeichen an Variablennamen gebunden (z.B. `int* pointerName`).
* **`const`:** An den Typ gebunden, zwischen Typ und Pointer-/Referenzzeichen (z.B. `double const pi`).
* **Initialisierung:** Bevorzugt mit Zuweisungs-Syntax (`=`).
* **`auto`:** Mit Bedacht einsetzen, kann Lesbarkeit verbessern.

### 3.3. Typedef

* **`using`** wird **`typedef`** vorgezogen (bessere Lesbarkeit, Template-Unterstützung).

### 3.4. Funktionen

* **Namen:** `CamelCase`, beginnend mit Großbuchstaben (z.B. `FunctionName`).
* Globale Funktionen mit `::` Präfix kennzeichnen.
* Meist imperativ (z.B. `Move`, `Close`).
* **Parameterliste:** Öffnende Klammer durch Leerzeichen vom Funktionsnamen getrennt.
* **Funktionsrumpf:** Öffnende geschweifte Klammer in neuer Zeile.
* **Parameternamen:** Präfix `the` und dann `CamelCase` (z.B. `theParameter`).
* Parameter, die nicht in eine Zeile passen, auf mehrere Zeilen aufteilen (ein Parameter pro Zeile, eingerückt).
* Parameternamen müssen in Deklaration und Definition übereinstimmen (bei Unbenutzung auskommentieren, nicht entfernen).
* **Übergabe von Typen:**
    * Benutzerdefinierte Typen: Als Referenzen (ggf. `const`-Referenzen).
    * Eingebaute Typen: Als Wert (niemals `const`-Referenzen).
* Funktionen sollten eine gewisse Länge nicht überschreiten (Refactoring anstreben).
* **`inline`:** Nur bei klarem Performance-Nutzen.
* **C-Style Variadic Functions (`...`):** Verboten (Typunsicherheit); Alternativen wie C++-Streams oder `std::format` nutzen.
* **Variadische Templates (C++11):** Erlaubt (Typsicherheit).

### 3.5. Kontrollstrukturen

* **`if`:** Leerzeichen nach `if`, keine Leerzeichen in Bedingungsparametern. Geschweifte Klammern optional bei einzelnen Anweisungen. `else` auf gleicher Zeile wie schließende Klammer. Explizite Vergleiche mit 0, `bool`-Ausdrücke direkt nutzen. Literale rechts in Vergleichen.
* **`for`:** Leerzeichen nach `for`, keine Leerzeichen in Kontrollanweisungen. Präfix-Inkrement/Dekrement (`++i`, `--i`) bevorzugen.
* **`while`:** Leerzeichen nach `while`, keine Leerzeichen in Bedingungsparametern.
* **`do-while`:** Rumpf immer in geschweifte Klammern, `while` auf gleicher Zeile nach schließender Rumpfklammer.
* **`switch`:** Leerzeichen nach `switch`, keine Leerzeichen in Ausdrucksparametern. `case`-Labels und Anweisungen eingerückt. `break` in neuer Zeile. Fall-through mit `[[fallthrough]]` (C++17) kennzeichnen. `default` immer als letzter Fall.

### 3.6. Typumwandlung

* **Verboten:** C-Style und Function-Style Casts.
* **Verwenden:** C++-Casts (`static_cast<>`, `const_cast<>`, `reinterpret_cast<>`, `dynamic_cast<>`).
* **Spezial-Casts:** `pointer_cast<>` (für `dynamic_cast<>` von Pointern, die Exception werfen sollen), `implicit_cast<>` (für implizite Umwandlungen).
* **`const_cast<>`:** Nur bei tatsächlich nicht-`const` Objekten oder defekten Schnittstellen.
* **`reinterpret_cast`:** Nur als letztes Mittel.

### 3.7. `sizeof`

* Ausdruck für `sizeof` immer in runde Klammern setzen.
* Variablennamen statt Typ bei `sizeof` bevorzugen.

### 3.8. Namensräume

* **Namen:** Kleingeschrieben, kurz, einwortig (z.B. `tools`).
* Inhalt nicht eingerückt.
* Öffnende geschweifte Klammer auf gleicher Zeile wie Namensraumname.
* Jedes Modul hat eigenen Namensraum.
* `// namespace <Name>`-Kommentar hinter schließender Klammer.
* Namensräume nur für Deklarationen und Klassendefinitionen öffnen.
* Anonyme Namensräume für lokale Helferkonstrukte in Implementierungsdateien (max. einer pro Datei).
* **In Headern verboten:** `using`-Deklarationen und `using namespace`-Direktiven.
* **In Implementierungsdateien erlaubt:** `using`-Deklarationen und `using namespace`-Direktiven.

### 3.9. Enumerationen

* **Namen:** `CamelCase` mit `E`-Präfix (z.B. `EWindowsVersion`).
* Öffnende geschweifte Klammer auf gleicher Zeile.
* **Alte Enums:** Werte mit kleingeschriebener Abkürzung des Enum-Namens, dann `CamelCase`.
* **Neue Enums (`enum class`):** Ohne Präfix, Großbuchstabe, dann `CamelCase`.
* Neue Enums sind zu bevorzugen.

### 3.10. Klassen

* **Namen:** `CamelCase` mit `C`-Präfix (z.B. `CStyleGuide`), gilt auch für Strukturen.
* **Ableitung:** Leerzeichen nach Klassennamen, Doppelpunkt, dann Ableitungsspezifikator (public, protected, private).
* Öffnende geschweifte Klammer auf gleicher Zeile wie letzte Basisklasse oder Klassenname.
* Maximal ein `public:`, `protected:`, `private:` Block in dieser Reihenfolge.
* Sichtbarkeitsspezifizierer auf gleicher Einrücktiefe wie `class`, Deklarationen eingerückt.
* **Reihenfolge der Deklarationen:** Standardkonstruktor, Kopierkonstruktor, andere Konstruktoren, Destruktor, (Leerzeile), Operatoren, (Leerzeile), Mitgliedsvariablen, Mitgliedsfunktionen.
* Mitgliedsfunktionen alphabetisch sortiert.
* Definition von Mitgliedsfunktionen innerhalb der Klassendefinition ist verboten.
* Inline-Member-Funktionen werden unterhalb der Klasse im Header definiert.
