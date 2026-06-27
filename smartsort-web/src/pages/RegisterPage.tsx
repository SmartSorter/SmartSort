import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { smartSortApi } from '../api/smartSortApi';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Alert, 
  Paper,
  MenuItem
} from '@mui/material';

export const RegisterPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('User'); 
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    if (!username || !password) {
      setError('Будь ласка, заповніть всі поля');
      return;
    }

    setSubmitting(true);

    try {
      await smartSortApi.register(username, password, role);
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Помилка під час реєстрації. Можливо, таке ім\'я вже зайняте.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={3} sx={{ padding: 4, width: '100%', borderRadius: 2 }}>
          <Typography component="h1" variant="h5" align="center" sx={{ fontWeight: 'bold', mb: 2 }}>
            Реєстрація SmartSorter
          </Typography>
          <Typography variant="body2" color="textSecondary" align="center" sx={{ mb: 3 }}>
            Створення нового облікового запису системи
          </Typography>

          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          {success && <Alert severity="success" sx={{ mb: 2 }}>Реєстрація успішна! Перенаправлення...</Alert>}

          <Box component="form" onSubmit={handleSubmit} noValidate>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Ім'я користувача (Логін)"
              name="username"
              autoComplete="username"
              autoFocus
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Пароль"
              type="password"
              id="password"
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            
            {/* Вибір ролі користувача */}
            <TextField
              select
              margin="normal"
              required
              fullWidth
              id="role"
              label="Роль у системі"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <MenuItem value="User">Диспетчер (User)</MenuItem>
              <MenuItem value="Admin">Адміністратор (Admin)</MenuItem>
            </TextField>

            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              disabled={submitting || success}
              sx={{ mt: 3, mb: 2, padding: '10px', fontWeight: 'bold' }}
            >
              {submitting ? 'Реєстрація...' : 'Зареєструватися'}
            </Button>

            <Box sx={{ textAlign: 'center', mt: 1 }}>
              <Link to="/login" style={{ textDecoration: 'none', color: '#1976d2', fontSize: '14px' }}>
                Вже є акаунт? Увійти
              </Link>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};