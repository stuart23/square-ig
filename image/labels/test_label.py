from .label import generate_label, generate_label_bytes


def test_generate_label(tmp_path):
    label = generate_label(
        sku='plantsoc.io/abcd1234',
        title='Pilea',
        variation='4"',
        price=123.45,
        pet_safe=True
    )
    label_file = tmp_path / 'label.png'
    label.save(label_file)
    assert label_file.is_file()


def test_generate_label_bytes(tmp_path):
    filename = 'Pilea-4.png'
    label_bytes = generate_label_bytes(
        filename=filename,
        sku='plantsoc.io/abcd1234',
        title='Pilea',
        variation='4"',
        price=123.45,
        pet_safe=True
    )
    assert label_bytes
    assert label_bytes.name == filename