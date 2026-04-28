export const getDashboardData = () => {
  return {
    aps: [
      { name: "Hormiguero-AP1", status: "online", usage: 40, lat: 3.375, lng: -76.548 },
      { name: "Montebello-AP1", status: "offline", usage: 0, lat: 3.451, lng: -76.57 },
      { name: "Castilla-AP1", status: "online", usage: 90, lat: 3.42, lng: -76.52 },
      { name: "Pance-AP1", status: "online", usage: 70, lat: 3.39, lng: -76.55 }
    ],
    kpis: { total: 23, online: 17, offline: 6, clients: 532 },
    charts: {
      users: [
        { time: "08:00", users: 120 },
        { time: "10:00", users: 220 },
        { time: "12:00", users: 300 },
        { time: "14:00", users: 280 },
        { time: "16:00", users: 350 }
      ],
      usage: [
        { name: "AP1", usage: 80 },
        { name: "AP2", usage: 45 },
        { name: "AP3", usage: 60 }
      ],
      status: [
        { name: "Online", value: 17 },
        { name: "Offline", value: 6 }
      ]
    }
  };
};