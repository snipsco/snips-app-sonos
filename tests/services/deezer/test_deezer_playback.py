from snipssonos.services.deezer.music_playback_service import DeezerNodeMusicPlaybackService


def test_play_returns_true():
    deezer_playback = DeezerNodeMusicPlaybackService()
    assert deezer_playback.play("a_device", "a_music_item") is True


def test_queue_returns_true():
    deezer_playback = DeezerNodeMusicPlaybackService()
    assert deezer_playback.queue("a_device", "a_music_item") is True
