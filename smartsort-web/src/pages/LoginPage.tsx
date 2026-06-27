import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { smartSortApi } from '../api/smartSortApi';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Alert, 
  Paper 
} from '@mui/material';

export const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    try {
      const data = await smartSortApi.login(username, password);
      login(data.access_token);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Неправильне ім\'я користувача або пароль');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={3} sx={{ padding: 4, width: '100%', borderRadius: 2 }}>
          <Typography component="h1" variant="h5" align="center" sx={{ fontWeight: 'bold', mb: 2 }}>
            SmartSorter Web
          </Typography>
          <Typography variant="body2" color="textSecondary" align="center" sx={{ mb: 3 }}>
            Панель керування та моніторингу баків
          </Typography>

          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

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
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={submitting}
              sx={{ mt: 3, mb: 2, padding: '10px', fontWeight: 'bold' }}
            >
              {submitting ? 'Вхід...' : 'Увійти'}
            </Button>

            <Box sx={{ textAlign: 'center', mt: 1 }}>
              <Link to="/register" style={{ textDecoration: 'none', color: '#1976d2', fontSize: '14px' }}>
                Немає облікового запису? Зареєструватися
              </Link>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};