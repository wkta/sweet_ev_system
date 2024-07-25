const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, 'transcrypt_config.json');
const pyScriptsDir = path.join(__dirname, 'py-scripts');
const jsScriptsDir = path.join(__dirname, 'js-scripts');

if (!fs.existsSync(jsScriptsDir)){
    fs.mkdirSync(jsScriptsDir);
}

fs.readdir(pyScriptsDir, (err, files) => {
    if (err) {
        console.error('Could not list the directory.', err);
        process.exit(1);
    }

    files.forEach((file, index) => {
        const filePath = path.join(pyScriptsDir, file);

        exec(`transcrypt -b -p .none -n ${filePath} -od ${jsScriptsDir}`, (error, stdout, stderr) => {  // the -p .none option here is extremely important. Its for 'nominative mode',
				    // otherwise we get ES6 format which will crash in server.js
						
            if (error) {
                console.error(`Error executing transcrypt on ${filePath}:`, error);
                return;
            }
						
						/*
            const jsFileName = file.replace('.py', '.js');
            const jsFilePath = path.join(pyScriptsDir, '__javascript__', jsFileName);

            if (fs.existsSync(jsFilePath)) {
                fs.copyFileSync(jsFilePath, path.join(jsScriptsDir, jsFileName));
                console.log(`Compiled and copied ${jsFileName}`);
            }
						*/

            /*if (index === files.length - 1) {
                // Clean up
                fs.rmdirSync(path.join(pyScriptsDir, '__javascript__'), { recursive: true });
                console.log('Clean up completed');
            }
						*/
						console.log('converted:', filePath);
        });
    });
});
