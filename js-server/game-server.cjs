const WebSocket = require('ws');
const path = require('path');
const fs = require('fs');

console.log('-----RUNNING EVO SERVER---');


const clients = [];
// ----------------------
// Expose the sendToClients function, to grant access from within transpiled code
global.sendToClients = (message) => {
    clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(message);
        }
    });
};
// ----------------------

const wss = new WebSocket.Server({ port: 8080 });
const scriptsDir = path.join(__dirname, 'js-scripts');

// Function to dynamically populate the scripts object
const getScripts = (dir) => {
    const scripts = {};
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        if (file.endsWith('.js') || file.endsWith('.cjs')) {
            scripts[file] = 'file://' + path.join(dir, file);
        }
    });

    return scripts;
};

const scripts = getScripts(scriptsDir);


// Include the transpiled Python code
import('./js-scripts/netw_node_server.js').then((netlayerPyModule)=> {
import('./js-scripts/server_component.js').then((serverPyModule)=> {

	// server compo doit register son mediator sur netlayer:
  serverPyModule.do_mediator_binding()

  // debug:
	// console.log('COUCOU', netlayerPyModule.get_server_flag() );

wss.on('connection', (ws, req) => {
    //const gkey = req.url.slice(1);
    //console.log('requested key:', gkey);
    
		//temporary do this:
		const gkey = 'artificial.js'

		const scriptPath = scripts[gkey];
    console.log('script:', scriptPath);

    if (!scriptPath) {
        console.log(`not a valid script path`);
        ws.close();
        return;
    }

    try {
					// Dynamically import the module
					import(scriptPath).then((module) => {
							console.log(`connect+script loading OK! Loaded script: ${gkey}:`);
							clients.push(ws);
							
							ws.on('message', (data) => {
									const strMessage = data.toString();
									// lien effectif avec netlayer
									netlayerPyModule.partie_reception(strMessage);

							});

							ws.on('close', () => {
									console.log(`Disconnected from ${gkey}`);
									const index = clients.indexOf(ws);
									if (index !== -1) {
											clients.splice(index, 1);
									}
							});

					}).catch((error) => {
							console.error(`Failed to load script for ${gkey}:`, error);
							ws.close();
					});


    } catch (error) {
        console.error(`Failed to run script for ${gkey}:`, error);
        ws.close();
    }
});



// ------------------- realtime ?-----------------
/*
import('./js-scripts/gamelogic.js').then((logicmodule)=>{
	
	const gameLoop = () => {  # game loop
			const currentTime = Date.now();
			const deltaTime = currentTime - lastUpdateTime;

			logicmodule.ss_gamelogic_update(currentTime);  # Update the server state here
			mediatorModule.refresh_event_queue()

			//Notify all clients of the updated state
			clients.forEach(client => {
					if (client.readyState === WebSocket.OPEN) {
							client.send(JSON.stringify({
									type: 'update',
									deltaTime: deltaTime,
									message: `Update received at ${new Date().toISOString()}`
							}));
					}
			});
			
			lastUpdateTime = currentTime;
	};
	setInterval(gameLoop, updateInterval);  # start the game loop
	console.log('gameloop started');
});
*/

// Game loop variables
let lastUpdateTime = Date.now();
const updateInterval = 500; // Update every 0.5 sec
const gameLoop = () => { 
		const currentTime = Date.now();
		const deltaTime = currentTime - lastUpdateTime;

		// et là on pourrait push un event EngineEvTypes.'update' aussi?

		serverPyModule.refresh_event_queue(); // Update the server state here

		//Notify all clients of the updated state
		/* clients.forEach(client => {
				if (client.readyState === WebSocket.OPEN) {
						client.send(JSON.stringify({
								type: 'update',
								deltaTime: deltaTime,
								message: `Update received at ${new Date().toISOString()}`
						}));
				}
		});
		lastUpdateTime = currentTime; */
};
setInterval(gameLoop, updateInterval); //started the game loop

});
});

console.log('Server is running on ws://localhost:8080');
