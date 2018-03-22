#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Fichier de configuration pour travailler sur le portail en local"""

from __future__ import print_function
import os, subprocess, sys

MODIFYING_DEVENV = False

DOCKER_V = "docker -v"
DOCKER_COMPOSE_V = "docker-compose -v"
CHECK_DOCKER_DAEMON_RUNNING = "docker stats --no-stream"
CHECK_NO_LOCAL_CHANGES = "git diff-index --quiet HEAD --"
PULL_DEVENV = "git pull"
START_PORTAIL = "docker-compose up"
CLONE_PORTAIL = "git clone https://github.com/UDEEMP/portail"
try:
	FileNotFoundError
except:
	FileNotFoundError = OSError

def run_command(command, log):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    while log:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc

print("Vérification de la configuration du portail")

print(" - Vérification de l'installation de Docker ... ", end='')
sys.stdout.flush()
try:
	process1 = subprocess.Popen(DOCKER_V.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	process2 = subprocess.Popen(DOCKER_COMPOSE_V.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except FileNotFoundError:
	# Docker is not installed
	print('❌\n\n')
	print("Impossible de démarrer docker et docker-compose")
	print("Installez Docker puis recommencez")
	print("https://www.docker.com/community-edition#/download")
	sys.exit()
print('✅')

print(" - Vérification du daemon Docker .............. ", end='')
sys.stdout.flush()
try:
	subprocess.check_call(CHECK_DOCKER_DAEMON_RUNNING.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
	# Docker daemon is not running
	print('❌\n\n')
	print("Le daemon Docker n'est pas disponible")
	print("Veuillez démarrer Docker")
	sys.exit()
print('✅')

print(" - Mise à jour de l'environnement ............. ", end='')
sys.stdout.flush()
if not MODIFYING_DEVENV:
	try:
		subprocess.check_call(CHECK_NO_LOCAL_CHANGES.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except subprocess.CalledProcessError:
		print('❌\n\n')
		print("Modifications non commit trouvées")
		print("Veuillez les supprimer")
		sys.exit()

	try:
		subprocess.check_call(PULL_DEVENV.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except subprocess.CalledProcessError:
		print('❌\n\n')
		print("Impossible de pull la dernière version du repo")
		sys.exit()
	print('✅')
else:
	print('⚠️  (Skipped for tests)')

if not (os.path.exists("./portail") and os.path.exists("./portail/.git")):
	print(" - Téléchargement du portail .................. ", end='')
	sys.stdout.flush()
	try:
		subprocess.check_call(CLONE_PORTAIL.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except subprocess.CalledProcessError:
		print('❌\n\n')
		print("Impossible de télécharger le portail")
		sys.exit()
	print('✅')
sys.stdout.flush()

try:
	subprocess.check_call(START_PORTAIL, shell=True)
except Excetion:
	pass









