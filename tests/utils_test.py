from unittest.mock import patch

from whis.utils import muted_print, ANSIColors


class TestMutedPrint:
    @patch("builtins.print")
    def test_muted_print(self, mock_print):
        muted_print("Lelolo lelo le!")

        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]

        assert "Lelolo lelo le!" in call_args
        assert ANSIColors.GRAY in call_args
        assert ANSIColors.RESET in call_args
