from unittest.mock import patch

from whis.utils import ANSIColors, colorize, get_whis_env_vars, print_muted


class TestMutedPrint:
    @patch("builtins.print")
    def test_print_muted(self, mock_print):
        print_muted("Lelolo lelo le!")

        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]

        assert "Lelolo lelo le!" in call_args
        assert ANSIColors.GRAY in call_args
        assert ANSIColors.RESET in call_args

    def test_colorize(self):
        assert colorize("foo", ANSIColors.GRAY) == (f"{ANSIColors.GRAY}foo{ANSIColors.RESET}")

    @patch.dict("os.environ", {"WHIS_TEST": "test", "OTHER": "value"}, clear=True)
    def test_get_whis_env_vars(self):
        result = get_whis_env_vars()
        assert result == {"WHIS_TEST": "test"}
