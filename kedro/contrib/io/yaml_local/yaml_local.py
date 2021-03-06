# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
#     or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""``YAMLLocalDataset`` loads and saves data to a local yaml file using
``PyYAML``.
See https://pyyaml.org/wiki/PyYAMLDocumentation for details.
"""
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import yaml

from kedro.contrib.io import DefaultArgumentsMixIn
from kedro.io.core import AbstractVersionedDataSet, Version, deprecation_warning


class YAMLLocalDataSet(DefaultArgumentsMixIn, AbstractVersionedDataSet):
    """``YAMLLocalDataset`` loads and saves data to a local yaml file using ``PyYAML``.
    See https://pyyaml.org/wiki/PyYAMLDocumentation for details.

    Example:
    ::

        >>> from kedro.contrib.io.yaml_local import YAMLLocalDataSet
        >>> my_dict = {
        >>>     'a_string': 'Hello, World!',
        >>>     'a_list': [1, 2, 3]
        >>> }
        >>> data_set = YAMLLocalDataSet(filepath="test.yml")
        >>> data_set.save(my_dict)
        >>> reloaded = data_set.load()
        >>> assert my_dict == reloaded

    """

    DEFAULT_SAVE_ARGS = {"default_flow_style": False}  # type: Dict[str, Any]

    def __init__(
        self, filepath: str, save_args: Dict[str, Any] = None, version: Version = None
    ) -> None:
        """Creates a new instance of ``YAMLLocalDataset`` pointing to a concrete
        filepath.

        Args:
            filepath: path to a local yaml file.
            save_args: Arguments passed on to ```yaml.dump``.
                See https://pyyaml.org/wiki/PyYAMLDocumentation for details.
                ``{"default_flow_style": False}`` in default.
            version: If specified, should be an instance of
                ``kedro.io.core.Version``. If its ``load`` attribute is
                None, the latest version will be loaded. If its ``save``
                attribute is None, save version will be autogenerated.

        """
        deprecation_warning(self.__class__.__name__)
        super().__init__(filepath=Path(filepath), save_args=save_args, version=version)

    def _describe(self) -> Dict[str, Any]:
        return dict(
            filepath=self._filepath, save_args=self._save_args, version=self._version
        )

    def _load(self) -> Any:
        load_path = Path(self._get_load_path())
        with load_path.open("r") as local_file:
            return yaml.safe_load(local_file)

    def _save(self, data: pd.DataFrame) -> None:
        save_path = Path(self._get_save_path())
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with save_path.open("w") as local_file:
            yaml.dump(data, local_file, **self._save_args)

    def _exists(self) -> bool:
        path = self._get_load_path()
        return Path(path).is_file()
