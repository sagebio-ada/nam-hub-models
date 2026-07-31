"""Validate the example instance data in data/ against the LinkML schema.

Gating runs through ``linkml-run-examples``, which is the only LinkML entry point
that reliably exits nonzero on an unexpected result. Two more obvious approaches
were ruled out because each produces a silently-passing test:

* the ``linkml-validate`` CLI prints ``[ERROR]`` lines for invalid data but still
  exits 0, so a CI step calling it directly never fails; and
* ``Validator(SchemaView(path).schema)`` drops the import closure, which leaves
  required slots and undefined properties entirely unchecked -- it reports
  data/invalid fixtures as clean.

data/problem holds cases the schema does not yet handle correctly, so it is
deliberately excluded here.

Checks on the fixtures themselves -- that their filenames name real classes, that they
use only declared slots -- need no validator run and live in OTHERtesting/ instead.
"""

import subprocess

from .conftest import INVALID_DIR, PORTAL_SCHEMA_DIR, VALID_DIR


def test_valid_examples_pass_and_counter_examples_fail(tmp_path):
    """The whole example corpus must behave as its directory placement claims.

    Files in data/valid MUST validate; files in data/invalid MUST
    NOT. linkml-run-examples enforces both directions and names the offending
    file in its error, so a failure here points straight at the fixture.
    """
    result = subprocess.run(
        [
            "linkml-run-examples",
            "--schema", str(PORTAL_SCHEMA_DIR / "namhub.yaml"),
            "--input-directory", str(VALID_DIR),
            "--counter-example-input-directory", str(INVALID_DIR),
            "--output-directory", str(tmp_path / "output"),
        ],
        capture_output=True,
        text=True,
        check=False,  # a nonzero exit is a real outcome here, asserted below
    )
    assert result.returncode == 0, (
        "example data did not behave as its directory placement claims\n\n"
        f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}"
    )
