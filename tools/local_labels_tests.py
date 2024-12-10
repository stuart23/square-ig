'''
Builds a directory of all the labels locally for testing changes. To generate a new set of (baseline) labels using the current code,
run `local_labels_tests.py generate`. Then to test new code changes, run it with `local_labels_tests.py compare`.

Requires:
```
pip install opencv-python scikit-image
```
'''

import sys
from os import environ
from pathlib import Path
import shutil

from skimage.metrics import structural_similarity
import cv2

pwd = Path(__file__).parent.resolve()
sys.path.append(str(pwd / '..' / 'image'))

environ['square_token_arn'] = 'arn:aws:secretsmanager:us-east-1:015140017687:secret:square_token-oMlH85'
from square_client import SquareClient
from labels.label import generate_label

tests_dir = pwd / "output" / "tests"
baseline_dir = pwd / "output" / "baseline"

def generate():
    '''
    Regenerates all the labels into the baseline directory.
    '''
    items = SquareClient().get_catalog_items()
    for item in items:
        baseline_file = baseline_dir / f'{item.sku_stem}.png'
        generate_label(item, image_output_file=baseline_file, debug=False)



def compare():
    '''
    Regenerates all the labels into the tests directory with comparisons to baseline.
    '''
    max_dir_number = 0
    for dir_name in tests_dir.iterdir():
        try:
            dir_number = int(dir_name.stem)
        except ValueError:
            continue
        if dir_number > max_dir_number:
            max_dir_number = dir_number
    output_dir = tests_dir / str(max_dir_number + 1)
    output_dir.mkdir()
    print(f'Generating in {output_dir}')

    raw_output = output_dir / "raw"
    raw_output.mkdir()
    raw_html_output = output_dir / "raw_html"
    raw_html_output.mkdir()
    html_debug_output = output_dir / "debug_html"
    html_debug_output.mkdir()
    png_debug_output = output_dir / "debug_png"
    png_debug_output.mkdir()
    differences_output = output_dir / "differences"
    differences_output.mkdir()

    items = SquareClient().get_catalog_items()

    for item in items:
        png_filename = raw_output / f'{item.sku_stem}.png'
        html_filename = raw_html_output / f'{item.sku_stem}.png'

        debug_html_filename = html_debug_output / f'{item.sku_stem}.html'
        debug_png_filename = png_debug_output / f'{item.sku_stem}.png'
        label = generate_label(item, image_output_file=debug_png_filename, html_output_file=debug_html_filename, debug=True)
        label = generate_label(item, image_output_file=png_filename, html_output_file=html_filename, debug=False)
        baseline_file = baseline_dir / f'{item.sku_stem}.png'

        print(f'New file {png_filename}')
        print(f'Baseline file {baseline_file}')
        assert baseline_file.exists()
        # Load images
        baseline = cv2.imread(baseline_file)
        new = cv2.imread(png_filename)

        # Convert images to grayscale
        baseline_gray = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
        new_gray = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)

        # Compute SSIM between the two images
        (score, diff) = structural_similarity(baseline_gray, new_gray, full=True)
        print("Image Similarity: {:.4f}%".format(score * 100))
        if score < 1:
            shutil.copy(png_filename, differences_output / f'{item.sku_stem}_b.png')
            shutil.copy(baseline_file, differences_output / f'{item.sku_stem}_a.png')

if __name__ == '__main__': 
    if sys.argv[-1] == 'generate':
        generate()
    elif argv[-1] == 'compare':
        compare()
    else:
        raise Exception("Pass 'generate' or 'compare' as an argument.")