# Auth Testing Playbook (saved per integration playbook instructions)

This file is the canonical Emergent Auth testing playbook for the JARVIS app.
The testing agent must read this BEFORE touching any auth-gated endpoint.

## Test User & Session creation
```bash
mongosh --eval "
use('jarvis_db');
var userId = 'test-user-' + Date.now();
var sessionToken = 'test_session_' + Date.now();
db.users.insertOne({
  user_id: userId,
  email: 'test.user.' + Date.now() + '@example.com',
  name: 'Test User',
  picture: 'https://via.placeholder.com/150',
  created_at: new Date()
});
db.user_sessions.insertOne({
  user_id: userId,
  session_token: sessionToken,
  expires_at: new Date(Date.now() + 7*24*60*60*1000),
  created_at: new Date()
});
print('Session token: ' + sessionToken);
print('User ID: ' + userId);
"
```

## Backend tests
```bash
# verify identity
curl -X GET "$URL/api/auth/me" -H "Authorization: Bearer $TOKEN"

# protected endpoint
curl -X GET "$URL/api/sessions" -H "Authorization: Bearer $TOKEN"

# create chat under that user
curl -X POST "$URL/api/chat" -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message":"hello"}'
```

## Browser test (Playwright)
```python
await page.context.add_cookies([{
  "name": "session_token",
  "value": TOKEN,
  "domain": "<your-domain>",
  "path": "/",
  "httpOnly": True,
  "secure": True,
  "sameSite": "None"
}])
await page.goto(f"https://<your-domain>/")
```

## Cleanup
```bash
mongosh --eval "
use('jarvis_db');
db.users.deleteMany({email: /test\.user\./});
db.user_sessions.deleteMany({session_token: /test_session/});
"
```

## Success indicators
- ✅ `/api/auth/me` returns user JSON
- ✅ `/api/sessions` returns sessions only for current user
- ✅ Without token: 401

## Implementation checklist
- [x] User documents have `user_id` (custom UUID), never expose `_id`
- [x] Sessions filter by `user_id`
- [x] All Mongo queries use `{"_id": 0}` projection
- [x] Cookie: `httponly=True`, `secure=True`, `samesite="none"`, `path="/"`
- [x] `Authorization: Bearer` header fallback supported
