const ytdl = require('ytdl-core');
const ffmpeg = require('fluent-ffmpeg');
const stream = require('stream');

module.exports = async (req, res) => {
    const videoUrl = req.body.url;

    if (!ytdl.validateURL(videoUrl)) {
        return res.json({ success: false, message: 'Invalid YouTube URL' });
    }

    const audioStream = ytdl(videoUrl, { quality: 'highestaudio' });

    res.setHeader('Content-Type', 'audio/mp3');
    res.setHeader('Content-Disposition', 'attachment; filename="audio.mp3"');

    audioStream.pipe(res);
};
