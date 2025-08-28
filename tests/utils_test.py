from unittest.mock import patch

from whis.utils import print_muted, ANSIColors


class TestMutedPrint:
    @patch("builtins.print")
    def test_print_muted(self, mock_print):
        print_muted("Lelolo lelo le!")

        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]

        assert "Lelolo lelo le!" in call_args
        assert ANSIColors.GRAY in call_args
        assert ANSIColors.RESET in call_args
