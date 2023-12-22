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
