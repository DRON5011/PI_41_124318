param(
    [string]$BackupPath = "C:\Users\user\Desktop\VKR\PI_41_124318\postgres\backups",
    [string]$ContainerName = "VKR_Postgres",
    [string]$DBName = "VKR_Database",
    [string]$DBUser = "postgres",
    [int]$KeepDays = 7
)
$DailyPath = "$BackupPath\daily"
$WeeklyPath = "$BackupPath\weekly"
$MonthlyPath = "$BackupPath\monthly"

New-Item -ItemType Directory -Force -Path $DailyPath
New-Item -ItemType Directory -Force -Path $WeeklyPath
New-Item -ItemType Directory -Force -Path $MonthlyPath

# Формируем имя файла с датой
$DateStr = Get-Date -Format "yyyyMMdd"
$DateTimeStr = Get-Date -Format "yyyyMMdd_HHmmss"
$DayOfWeek = (Get-Date).DayOfWeek
$DayOfMonth = (Get-Date).Day

Write-Host "Начинаем создание бэкапа..." -ForegroundColor Green

try {
    $containerStatus = docker ps --filter "name=$ContainerName" --format "table {{.Status}}"
    if (-not $containerStatus) {
        throw "Контейнер $ContainerName не запущен!"
    }

    $dailyFile = "$DailyPath\vkr_$DateTimeStr.sql"
    Write-Host "📁 Создаем ежедневный бэкап: $dailyFile"
    docker exec $ContainerName pg_dump -U $DBUser -d $DBName > $dailyFile
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Ежедневный бэкап создан: $dailyFile" -ForegroundColor Green
        Compress-Archive -Path $dailyFile -DestinationPath "$dailyFile.zip" -Force
        Remove-Item $dailyFile
        Write-Host "Файл сжат: $dailyFile.zip" -ForegroundColor Green
    } else {
        throw "Ошибка при создании бэкапа!"
    }

    if ($DayOfWeek -eq "Monday") {
        $weeklyFile = "$WeeklyPath\vkr_weekly_$DateStr.sql"
        Write-Host "Создаем еженедельный бэкап: $weeklyFile"
        docker exec $ContainerName pg_dump -U $DBUser -d $DBName > $weeklyFile
        Compress-Archive -Path $weeklyFile -DestinationPath "$weeklyFile.zip" -Force
        Remove-Item $weeklyFile
        Write-Host "Еженедельный бэкап создан" -ForegroundColor Green
    }

    if ($DayOfMonth -eq 15) {
        $monthlyFile = "$MonthlyPath\vkr_monthly_$DateStr.sql"
        Write-Host "Создаем ежемесячный бэкап: $monthlyFile"
        docker exec $ContainerName pg_dump -U $DBUser -d $DBName > $monthlyFile
        Compress-Archive -Path $monthlyFile -DestinationPath "$monthlyFile.zip" -Force
        Remove-Item $monthlyFile
        Write-Host "Ежемесячный бэкап создан" -ForegroundColor Green
    }
    Write-Host "Очистка старых бэкапов (старше $KeepDays дней)..." -ForegroundColor Yellow
    Get-ChildItem -Path $DailyPath -Recurse | Where-Object { $_.CreationTime -lt (Get-Date).AddDays(-$KeepDays) } | Remove-Item -Force
    Write-Host "Очистка завершена" -ForegroundColor Green

    $logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Бэкап создан: $DateTimeStr - Размер: $((Get-Item "$dailyFile.zip").Length / 1MB) MB"
    Add-Content -Path "$BackupPath\backup.log" -Value $logEntry
    
    Write-Host "Бэкап успешно завершен!" -ForegroundColor Green
    
} catch {
    Write-Host "Ошибка: $_" -ForegroundColor Red
    
    # Отправка уведомления (опционально)
    $errorLog = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - ОШИБКА: $_"
    Add-Content -Path "$BackupPath\error.log" -Value $errorLog
}