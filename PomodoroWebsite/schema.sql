-- Create Users Table
CREATE TABLE "users" (
    "userid" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    "username" TEXT UNIQUE NOT NULL, 
    "password" TEXT NOT NULL, 
    "email" TEXT UNIQUE NOT NULL
);

-- Create PomodoroSettings Table
CREATE TABLE "PomodoroSettings" (
    "SettingID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "UserID" INTEGER,
    "WorkInterval" INTEGER DEFAULT 25,
    "ShortBreakInterval" INTEGER DEFAULT 5,
    "LongBreakInterval" INTEGER DEFAULT 15,
    FOREIGN KEY ("UserID") REFERENCES "users"("userid")
);

-- Create PomodoroLogs Table
CREATE TABLE "PomodoroLogs" (
    "LogID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "UserID" INTEGER,
    "Note" TEXT,
    FOREIGN KEY ("UserID") REFERENCES "users"("userid")
);

-- Create UserSettingsView View
CREATE VIEW "UserSettingsView" AS
SELECT u."username", p."WorkInterval", p."ShortBreakInterval", p."LongBreakInterval"
FROM "users" u
JOIN "PomodoroSettings" p ON u."userid" = p."UserID";

-- Create AfterUserCreation Trigger
CREATE TRIGGER "AfterUserCreation"
AFTER INSERT ON "users"
BEGIN
    INSERT INTO "PomodoroSettings" ("UserID") VALUES (NEW."userid");
END;