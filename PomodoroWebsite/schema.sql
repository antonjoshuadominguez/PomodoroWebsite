-- Create the 'users' table
CREATE TABLE "users" (
    "userid" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    "username" TEXT UNIQUE NOT NULL, 
    "password" TEXT NOT NULL, 
    "email" TEXT UNIQUE NOT NULL
);

-- Create the 'PomodoroSettings' table
CREATE TABLE "PomodoroSettings" (
    "SettingID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "UserID" INTEGER,
    "WorkInterval" INTEGER DEFAULT 25,
    "ShortBreakInterval" INTEGER DEFAULT 5,
    "LongBreakInterval" INTEGER DEFAULT 15,
    FOREIGN KEY ("UserID") REFERENCES "users"("userid")
);

-- Create the 'PomodoroLogs' table
CREATE TABLE "PomodoroLogs" (
    "LogID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "UserID" INTEGER,
    "Note" TEXT,
    FOREIGN KEY ("UserID") REFERENCES "users"("userid")
);

-- Create the 'AfterUserCreation' trigger
CREATE TRIGGER "AfterUserCreation"
AFTER INSERT ON "users"
BEGIN
    INSERT INTO "PomodoroSettings" ("UserID") VALUES (NEW."userid");
END;

-- Create the 'UserSettingsView' view
CREATE VIEW "UserSettingsView" AS
SELECT
    u.username AS "username",
    ps.WorkInterval AS "WorkInterval",
    ps.ShortBreakInterval AS "ShortBreakInterval",
    ps.LongBreakInterval AS "LongBreakInterval"
FROM
    "users" u
JOIN
    "PomodoroSettings" ps ON u.userid = ps.UserID;


CREATE VIEW ProcedureView AS
SELECT
    u.username,
    COUNT(l.LogID) AS TotalSessions,
    AVG(p.WorkInterval) AS AverageWorkInterval
FROM
    users u
JOIN
    PomodoroLogs l ON u.userid = l.UserID
JOIN
    PomodoroSettings p ON u.userid = p.UserID
GROUP BY
    u.username;