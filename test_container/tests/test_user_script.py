# Testet z. B. eine Funktion namens 'add'
import pytest

import user_script  # Importiertes User-Skript

def test_add():
    assert user_script.add(2, 3) == 5