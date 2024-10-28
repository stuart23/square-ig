from .qr_leaf import QRLeaf


def test_colour_qr(tmp_path):
    qr = QRLeaf(code_text='plantsoc.app/asdf1234')
    output_file = tmp_path / 'colour.png'
    qr.colour_qr.save(output_file)
    assert output_file.is_file()

def test_bw_qr(tmp_path):
    qr = QRLeaf(code_text='plantsoc.app/asdf1234')
    output_file = tmp_path / 'bw.png'
    qr.bw_qr.save(output_file)
    assert output_file.is_file()