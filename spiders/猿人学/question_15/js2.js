const fs = require('fs');
const buf = fs.readFileSync('./main.wasm');
window = {};
function toUint8Array(buf) {
    var u = new Uint8Array(buf.length);
    for (var i = 0; i < buf.length; ++i) {
        u[i] = buf[i];
    }
    return u;
}
WebAssembly.instantiate(toUint8Array(buf)).then(results => {
    instance = results.instance;
    q = instance.exports.encode;
    window.m = function () {
        t1 = parseInt(Date.parse(new Date()) / 1000 / 2);
        t2 = parseInt(Date.parse(new Date()) / 1000 / 2 - Math.floor(Math.random() * (50) + 1));
        return q(t1, t2).toString() + '|' + t1 + '|' + t2;
    }
    console.log(window.m())
});
