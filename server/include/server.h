/*
** EPITECH PROJECT, 2018
** PSU_zappy_2017
** File description:
** server.h
*/

#pragma once

#include <stddef.h>
#include "poll/src/common.h"
#include "list/src/list.h"

#define RBUFFER_SIZE 4096
#define CMD_SIZE 2048

typedef struct rbuf_s {
	char buffer[RBUFFER_SIZE];
	int start;
	int end;
	int size;
} rbuf_t;

typedef struct cmd_s {
	rbuf_t rbuf;
	char cmd[CMD_SIZE];
	char name[CMD_SIZE];
	char **param;
	int nparam;
} cmd_t;

typedef struct params_s {
	size_t port;
	size_t width;
	size_t height;
	char **teams;
	size_t nclt;
	size_t tickrate;
} params_t;
typedef struct vec2_s {
	size_t x;
	size_t y;
} vec2_t;

typedef struct client_s {
	int fd;
	cmd_t cmd;
	size_t id;
	vec2_t pos;
	size_t food;
} client_t;

typedef struct control_s {
	poll_t *list;
	list_t *clients;
} control_t;

typedef struct tuple_s {
	char *cmd;
	void (*func)(control_t *, client_t *);
} tuple_t;

void cmd_msv(control_t *, client_t *);
void cmd_bct(control_t *, client_t *);
void cmd_mct(control_t *, client_t *);
void cmd_tna(control_t *, client_t *);
void cmd_ppo(control_t *, client_t *);
void cmd_plv(control_t *, client_t *);
void cmd_pin(control_t *, client_t *);
void cmd_sgt(control_t *, client_t *);
void cmd_sst(control_t *, client_t *);