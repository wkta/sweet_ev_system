"""
Régle du jeu :
y a une >INTERFACE COMMUNE< à tous les fichiers netw_*


Ainsi, on doit exposer
----------------------

- get_server_flag() -> int

- start_comms(host_info, port_info)

- broadcast(evtype, evcontent) -> None

- register_mediator( obj ) où obj est un objet respectant l'interface de UMediator. CAR on call mediator.post( x, y, z)
  cela modifie effectivement l'état du NetworkLayer qui ne se réduit donc pas un paquet de methodes statiques


"""