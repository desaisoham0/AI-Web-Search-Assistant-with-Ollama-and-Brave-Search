def test_imports():
    import importlib

    assert importlib.import_module("langchain")
    assert importlib.import_module("rich")
