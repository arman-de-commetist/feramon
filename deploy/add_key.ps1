# One-time: put this computer's SSH key on the MONA server, so later uploads/updates need no password.
# You will be asked for the root password once: type it by hand (nothing is shown) and press Enter.
$key = (Get-Content "$env:USERPROFILE\.ssh\mona_server.pub" -Raw).Trim()
Write-Host ""
Write-Host "Type the root password (it is invisible) and press Enter:" -ForegroundColor Yellow
ssh -o StrictHostKeyChecking=accept-new -o PreferredAuthentications=password -o PubkeyAuthentication=no root@89.207.249.110 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '$key' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && echo KEY-INSTALLED"
