from .qr_code import QRCode


def test_colour_qr(tmp_path):
    qr = QRCode(code_text='plantsoc.app/asdf1234')
    output_file = tmp_path / 'colour_plain.png'
    output_file.unlink(missing_ok=True)
    assert not output_file.is_file()
    qr.colour_qr.save(output_file)
    assert output_file.is_file()
    output_file.unlink()


def test_bw_qr(tmp_path):
    qr = QRCode(code_text='plantsoc.app/asdf1234')
    output_file = tmp_path / 'bw_plain.png'
    output_file.unlink(missing_ok=True)
    assert not output_file.is_file()
    qr.bw_qr.save(output_file)
    assert output_file.is_file()
    output_file.unlink()