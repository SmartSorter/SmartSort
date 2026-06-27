import React, { useEffect, useState } from 'react';
import { smartSortApi } from '../api/smartSortApi';
import { useAuth } from '../context/AuthContext';
import { 
  Container, Grid, Paper, Typography, Button, Table, 
  TableBody, TableCell, TableContainer, TableHead, TableRow, 
  Alert, Box, LinearProgress, Dialog, DialogTitle, 
  DialogContent, DialogActions, TextField, MenuItem 
} from '@mui/material';
import axiosClient from '../api/axiosClient';

interface ContainerData {
  id: number;
  device_id: number;
  waste_type_id: number;
  fill_level: number;
}

interface AlertData {
  id: number;
  container_id: number;
  message: string;
}

interface DeviceData {
  id: number;
  serial_number: string;
  location: string | null;
}

interface WasteTypeData {
  id: number;
  name: string;
}

export const DashboardPage: React.FC = () => {
  const { logout, role } = useAuth();
  
  const [containers, setContainers] = useState<ContainerData[]>([]);
  const [alerts, setAlerts] = useState<AlertData[]>([]);
  const [devices, setDevices] = useState<DeviceData[]>([]);
  const [wasteTypes, setWasteTypes] = useState<WasteTypeData[]>([]);
  
  const [loading, setLoading] = useState(true);
  const [routeInfo, setRouteInfo] = useState<string | null>(null);

  const [openModal, setOpenModal] = useState(false);
  const [newDeviceId, setNewDeviceId] = useState('');
  const [newWasteTypeId, setNewWasteTypeId] = useState('');
  const [newFillLevel, setNewFillLevel] = useState(0);

  const fetchData = async () => {
    try {
      const [containersData, alertsData, devicesData, wasteTypesData] = await Promise.all([
        smartSortApi.getContainers(),
        smartSortApi.getAlerts(),
        smartSortApi.getDevices(),
        smartSortApi.getWasteTypes()
      ]);
      setContainers(containersData);
      setAlerts(alertsData);
      setDevices(devicesData);
      setWasteTypes(wasteTypesData);
    } catch (error) {
      console.error("Помилка завантаження даних системи:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleOptimize = async () => {
    try {
      const data = await smartSortApi.optimizeRoutes();
      setRouteInfo(data.description || "Маршрут успішно побудований логістичним модулем!");
    } catch (error) {
      setRouteInfo("Помилка під час генерації оптимального шляху");
    }
  };

  const handleCreateContainer = async () => {
    if (!newDeviceId || !newWasteTypeId) return;
    try {
      await axiosClient.post('/containers/', {
        device_id: Number(newDeviceId),
        waste_type_id: Number(newWasteTypeId),
        fill_level: Number(newFillLevel)
      });
      setOpenModal(false);
      setNewDeviceId('');
      setNewWasteTypeId('');
      setNewFillLevel(0);
      fetchData();
    } catch (error) {
      alert("Не вдалося створити контейнер. Перевірте коректність ID прив'язок.");
    }
  };

  if (loading) return <LinearProgress />;

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
            Веб-консоль SmartSorter
          </Typography>
          <Typography variant="subtitle2" color="textSecondary">
            Рівень доступу: <strong style={{ color: role === 'Admin' ? '#d32f2f' : '#1976d2' }}>{role === 'Admin' ? 'Адміністратор' : 'Диспетчер'}</strong>
          </Typography>
        </Box>
        <Button variant="outlined" color="error" onClick={logout}>
          Вийти
        </Button>
      </Box>

      <Grid container spacing={3}>
        <Grid size={12}>
          <Paper sx={{ p: 3, display: 'flex', flexDirection: 'row', gap: 2, flexWrap: 'wrap' }}>
            <Button variant="contained" color="primary" size="large" onClick={handleOptimize} sx={{ flexGrow: 1 }}>
              Запустити оптимізацію маршрутів
            </Button>
            
            {role === 'Admin' && (
              <Button variant="contained" color="secondary" size="large" onClick={() => setOpenModal(true)} sx={{ flexGrow: 1 }}>
                + Зареєструвати новий бак
              </Button>
            )}
          </Paper>
          {routeInfo && (
            <Alert severity="info" sx={{ mt: 2 }}>
              {routeInfo}
            </Alert>
          )}
        </Grid>

        {alerts.length > 0 && (
          <Grid size={12}>
            <Typography variant="h6" color="error" sx={{ mb: 1, fontWeight: 'bold' }}>
              Критичні системні сповіщення ({alerts.length})
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              {alerts.map((alert) => (
                <Alert key={alert.id} severity="warning">
                  Контейнер #{alert.container_id}: {alert.message}
                </Alert>
              ))}
            </Box>
          </Grid>
        )}

        <Grid size={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Моніторинг парку сміттєвих контейнерів</Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                    <TableCell sx={{ fontWeight: 'bold' }}>ID Контейнера</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Адреса / Локація датчика</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Категорія відходів</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Заповненість датчика IoT</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {containers.map((container) => {
                    const wasteType = wasteTypes.find(w => w.id === container.waste_type_id);
                    const device = devices.find(d => d.id === container.device_id);

                    return (
                      <TableRow key={container.id}>
                        <TableCell sx={{ fontWeight: 'bold' }}>Бак #{container.id}</TableCell>
                        <TableCell>{device ? device.location : `Датчик ID ${container.device_id}`}</TableCell>
                        <TableCell>{wasteType ? wasteType.name : `Тип ID ${container.waste_type_id}`}</TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                            <Box sx={{ width: '100%' }}>
                              <LinearProgress 
                                variant="determinate" 
                                value={Math.min(container.fill_level, 100)} 
                                color={container.fill_level >= 80 ? "error" : "success"}
                              />
                            </Box>
                            <Typography variant="body2" sx={{ fontWeight: 'bold', minWidth: '40px' }}>
                              {container.fill_level}%
                            </Typography>
                          </Box>
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>

      <Dialog open={openModal} onClose={() => setOpenModal(false)} fullWidth maxWidth="xs">
        <DialogTitle sx={{ fontWeight: 'bold' }}>Нова точка збору</DialogTitle>
        <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
          
          <TextField
            select
            label="Прив'язати IoT Пристрій"
            value={newDeviceId}
            onChange={(e) => setNewDeviceId(e.target.value)}
            fullWidth
            margin="dense"
          >
            {devices.map((d) => (
              <MenuItem key={d.id} value={d.id}>
                ID {d.id} - {d.location || 'Без локації'} ({d.serial_number})
              </MenuItem>
            ))}
          </TextField>

          <TextField
            select
            label="Тип відходів для переробки"
            value={newWasteTypeId}
            onChange={(e) => setNewWasteTypeId(e.target.value)}
            fullWidth
            margin="dense"
          >
            {wasteTypes.map((w) => (
              <MenuItem key={w.id} value={w.id}>
                {w.name}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            label="Поточний рівень заповнення (%)"
            type="number"
            value={newFillLevel}
            onChange={(e) => setNewFillLevel(Number(e.target.value))}
            fullWidth
            margin="dense"
            slotProps={{ htmlInput: { min: 0, max: 100 } }}
          />
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={() => setOpenModal(false)} color="inherit">Скасувати</Button>
          <Button onClick={handleCreateContainer} variant="contained" color="secondary">Створити</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};