# Workflow
please follow the workflow to ensure the commit tree is clean, and so that your progress won't be lost in the commit tree

## environment setup (one time only)

### 1. Fork the repo on GitHub website first!

### 2. Clone YOUR personal fork
```bash
git clone git@github.com:YOUR_USERNAME/market-connect-api.git
```

### 3. Enter folder
```bash
cd market-connect-api
```

### 4. Link to the "Holy Grail" (The main repo where the team collaborates)
```bash
git remote add upstream git@github.com:USERNAME/market-connect-api.git
```

### 5. Prevent accidents (Make it impossible to push to upstream directly)
```bash
git remote set-url --push upstream no_push
```

## daily development
### 1. Update your Local Main (Get latest changes from friends)
```bash
git checkout main
git fetch upstream          # Download latest info from Holy Grail
git rebase upstream/main    # Move your local main to match Holy Grail perfectly
```

### 2. Create a Branch for your work
```bash
git checkout -b feature/booking-logic
```

### 3. Work, Work, Work...
```bash
git add .
git commit -m "COMMIT MESSAGE"
# remember to type the commit message: a brief explanation about what you changed
```

### 4. The "Safety Check" (Crucial!)
Before you share your work, check if anyone else updated the Holy Grail while you were working.
```bash
git fetch upstream
git rebase upstream/main
```

### 5. Push to YOUR playground (Origin)
If you rebased in step 4, you might need -f, but usually first push is fine.
```bash
git push origin feature/booking-logic
# DO NOT PULL!!!
# add -f if the push didn't work
```