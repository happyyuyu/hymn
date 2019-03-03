const {app, BrowserWindow} = require('electron');
var zerorpc = require("zerorpc");

var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

client.invoke("hello", "RPC", function(error, res, more) {
    console.log(res);
});
// let {PythonShell} = require('python-shell')

function createWindow(){
    window = new BrowserWindow({width: 800, height: 600})
    window.loadFile('index.html')
    
    let options = {
        mode: 'text',
        scriptPath: './'
    }

    window.loadFile('index.html')
    // window.webContents.openDevTool();
    window.on('closed', function () {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        window = null
    })
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    // On macOS stays active unless user quits explicitly.
    if (process.platform !== 'darwin'){
        app.quit()
    } 
})

app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (mainWindow === null) {
      createWindow()
    }
})