from show import Show
from show_manager import ShowManager


def test_with_empty_input():
    show_manager = ShowManager(shows=[])

    result = show_manager.get_desired_destination("")

    assert result == ""


def test_non_found_series():
    show_manager = ShowManager(shows=[])

    result = show_manager.get_desired_destination(
        "/mnt/h/Download/The.Ciccios.s01e02.mkv"
    )

    assert result == ""


def test_when_there_are_files_not_in_folders():
    show_manager = ShowManager(
        shows=[Show(name="beingerica", dest_path="/mnt/h/Video/Serie/Being Erica")]
    )

    result = show_manager.get_desired_destination(
        "/mnt/h/Download/Being.Erica.4x03.Baby.Mama.HDTV.XviD-2HD.avi"
    )

    assert (
        result
        == "/mnt/h/Video/Serie/Being Erica/Being.Erica.4x03.Baby.Mama.HDTV.XviD-2HD.avi"
    )


def test_when_there_are_files_in_folders():
    show_manager = ShowManager(
        shows=[Show(name="beingerica", dest_path="/mnt/h/Video/Serie/Being Erica")]
    )

    result = show_manager.get_desired_destination(
        "/mnt/h/Download/Being.Erica.4x03/Being.Erica.4x03.Baby.Mama.HDTV.XviD-2HD.avi"
    )

    assert (
        result
        == "/mnt/h/Video/Serie/Being Erica/Being.Erica.4x03.Baby.Mama.HDTV.XviD-2HD.avi"
    )


def test_convert_season_series_format_to_x_series_format():
    show_manager = ShowManager(
        shows=[Show(name="beingerica", dest_path="/mnt/h/Video/Serie/Being Erica")]
    )

    result = show_manager.get_desired_destination(
        "/mnt/h/Download/Being.Erica.s4e03.Baby.Mama.HDTV.XviD-2HD.avi"
    )

    assert (
        result
        == "/mnt/h/Video/Serie/Being Erica/Being.Erica.4x03.Baby.Mama.HDTV.XviD-2HD.avi"
    )


def test_convert_season_series_format_to_x_series_format_when_season_has_double_digits():
    show_manager = ShowManager(
        shows=[Show(name="beingerica", dest_path="/mnt/h/Video/Serie/Being Erica")]
    )

    result = show_manager.get_desired_destination(
        "/mnt/h/Download/Being.Erica.s12e01.Baby.Mama.HDTV.XviD-2HD.avi"
    )

    assert (
        result
        == "/mnt/h/Video/Serie/Being Erica/Being.Erica.12x01.Baby.Mama.HDTV.XviD-2HD.avi"
    )


def test_move_also_files_with_parent_folder_matching_series_name():
    show_manager = ShowManager(
        shows=[
            Show(
                name="houseofthedragon",
                dest_path="/mnt/h/Video/Serie/House of the dragon",
            )
        ]
    )

    result = show_manager.get_desired_destination(
        "/mnt/h/Download/house of the dragon/7339d65e18834b79a923ff46fedc1210[EZTVx.to].mkv"
    )

    assert (
        result
        == "/mnt/h/Video/Serie/House of the dragon/7339d65e18834b79a923ff46fedc1210[EZTVx.to].mkv"
    )

def test_multiple_hits_creates_conflict():
    show_manager = ShowManager(
        shows=[
            Show(
                name="houseofthedragon",
                dest_path="/mnt/h/Video/Serie/House of the dragon",
            ),
            Show(
                name="beingerica",
                dest_path="/mnt/h/Video/Serie/Beeing Erica",
            ),
        ]
    )

    result = show_manager.get_desired_destination(
        "/mnt/h/Download/house of the dragon/being erica s3e01.avi"
    )

    assert (
        result
        == ""
    )