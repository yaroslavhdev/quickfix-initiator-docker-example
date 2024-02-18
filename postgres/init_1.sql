create database quick_fix_initiator;

\c quick_fix_initiator;

CREATE SEQUENCE event_log_sequence;

CREATE TABLE event_log
(
    id                INTEGER DEFAULT NEXTVAL('event_log_sequence'),
    time              TIMESTAMP NOT NULL,
    beginstring       CHAR(8),
    sendercompid      VARCHAR(64),
    targetcompid      VARCHAR(64),
    session_qualifier VARCHAR(64),
    text              TEXT      NOT NULL,
    PRIMARY KEY (id)
);

CREATE SEQUENCE event_backup_log_sequence;

CREATE TABLE event_backup_log
(
    id                INTEGER DEFAULT NEXTVAL('event_backup_log_sequence'),
    time              TIMESTAMP NOT NULL,
    beginstring       CHAR(8),
    sendercompid      VARCHAR(64),
    targetcompid      VARCHAR(64),
    session_qualifier VARCHAR(64),
    text              TEXT      NOT NULL,
    PRIMARY KEY (id)
);

CREATE SEQUENCE messages_log_sequence;

CREATE TABLE messages_log
(
    id                INTEGER DEFAULT NEXTVAL('messages_log_sequence'),
    time              TIMESTAMP NOT NULL,
    beginstring       CHAR(8),
    sendercompid      VARCHAR(64),
    targetcompid      VARCHAR(64),
    session_qualifier VARCHAR(64),
    text              TEXT      NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE messages
(
    beginstring       CHAR(8)     NOT NULL,
    sendercompid      VARCHAR(64) NOT NULL,
    targetcompid      VARCHAR(64) NOT NULL,
    session_qualifier VARCHAR(64) NOT NULL,
    msgseqnum         INTEGER     NOT NULL,
    message           TEXT        NOT NULL,
    PRIMARY KEY (beginstring, sendercompid, targetcompid, session_qualifier, msgseqnum)
);

CREATE TABLE sessions
(
    beginstring       CHAR(8)     NOT NULL,
    sendercompid      VARCHAR(64) NOT NULL,
    targetcompid      VARCHAR(64) NOT NULL,
    session_qualifier VARCHAR(64) NOT NULL,
    creation_time     TIMESTAMP   NOT NULL,
    incoming_seqnum   INTEGER     NOT NULL,
    outgoing_seqnum   INTEGER     NOT NULL,
    PRIMARY KEY (beginstring, sendercompid, targetcompid, session_qualifier)
);
