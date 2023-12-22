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