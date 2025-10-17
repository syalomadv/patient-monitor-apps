import numpy as np
from PySide6.QtCore import QThread, Signal
import time
from datetime import datetime

class DataWorker(QThread):
    data_ready = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.sample_rate = 200
        self.buffer_size = 1024
        self.hr = 75
        self.rr = 18
        self.time = 0.0
    
    def run(self):
        while self.running:
            self.generate_data()
            time.sleep(0.05)
    
    def stop(self):
        self.running = False
    
    def generate_data(self):
        t = np.linspace(self.time, self.time + self.buffer_size / self.sample_rate, self.buffer_size)
        self.time += self.buffer_size / self.sample_rate
        
        hr_period = 60 / self.hr
        rr_period = 60 / self.rr
        
        ecg = self.ecg_waveform(t, hr_period)
        
        pleth = self.pleth_waveform(t, hr_period)
        
        resp = self.resp_waveform(t, rr_period)
        
        art = self.art_waveform(t, hr_period)
        
        co2 = self.co2_waveform(t, rr_period)
        
        waveforms = {
            'ecg': ecg,
            'pleth': pleth,
            'resp': resp,
            'art': art,
            'co2': co2
        }
        
        vitals = self.compute_vitals(ecg, pleth, resp, art, co2, t)
        
        self.data_ready.emit({'waveforms': waveforms, 'vitals': vitals})
    
    def ecg_waveform(self, t, period):
        phase = (t % period) / period
        ecg = np.zeros_like(t)

        p_start = 0.1 * period
        p_end = 0.2 * period
        mask_p = (t % period >= p_start) & (t % period <= p_end)
        ecg[mask_p] = 0.1 * np.sin(2 * np.pi * (t[mask_p] - p_start) / (p_end - p_start))

        q_center = 0.22 * period
        mask_q = np.abs(t % period - q_center) < 0.01 * period
        ecg[mask_q] = -0.2 * np.exp(-((t[mask_q] - q_center)**2 / (0.005 * period)**2))

        r_center = 0.25 * period
        mask_r = np.abs(t % period - r_center) < 0.005 * period
        ecg[mask_r] = 1.0 * np.exp(-((t[mask_r] - r_center)**2 / (0.002 * period)**2))

        s_center = 0.28 * period
        mask_s = np.abs(t % period - s_center) < 0.01 * period
        ecg[mask_s] = -0.15 * np.exp(-((t[mask_s] - s_center)**2 / (0.005 * period)**2))

        t_start = 0.35 * period
        t_end = 0.55 * period
        mask_t = (t % period >= t_start) & (t % period <= t_end)
        ecg[mask_t] = 0.3 * np.sin(np.pi * (t[mask_t] - t_start) / (t_end - t_start)) * np.exp(-((t[mask_t] - 0.45 * period)**2 / (0.05 * period)**2))

        ecg += 0.05 * np.sin(2 * np.pi * t / (10 * period))
        ecg += 0.02 * np.random.randn(len(t))

        return ecg
    
    def pleth_waveform(self, t, period):
        pleth = 98 + 2 * np.sin(2 * np.pi * t / period)
        notch_time = 0.4 * period
        mask_notch = np.abs(t % period - notch_time) < 0.02 * period
        pleth[mask_notch] -= 0.5 * np.exp(-((t[mask_notch] - notch_time)**2 / (0.01 * period)**2))
        pleth += 0.1 * np.random.randn(len(t))
        return np.clip(pleth, 90, 100)
    
    def resp_waveform(self, t, period):
        resp = np.sin(2 * np.pi * t / period)
        resp += 0.1 * np.sin(4 * np.pi * t / period)
        resp += 0.05 * np.random.randn(len(t))
        return resp
    
    def art_waveform(self, t, period):
        art = np.zeros_like(t)
        systolic_peak = 120
        diastolic_base = 80

        for i in range(len(t)):
            tau = t[i] % period

            if tau < 0.3 * period:
                art[i] = diastolic_base + (systolic_peak - diastolic_base) * (1 - np.exp(-tau / (0.1 * period)))
            elif tau < 0.4 * period:
                time_from_peak = tau - 0.3 * period
                art[i] = systolic_peak - 5 * (time_from_peak / (0.1 * period))**2
                if time_from_peak > 0.05 * period:
                    art[i] -= 10 * np.exp(-(time_from_peak - 0.05 * period) / (0.02 * period))
            else:
                time_from_peak = tau - 0.3 * period
                art[i] = systolic_peak * np.exp(-time_from_peak / (0.4 * period)) + diastolic_base * (1 - np.exp(-time_from_peak / (0.4 * period)))

            art[i] = max(art[i], diastolic_base)

        art += 1 * np.sin(2 * np.pi * t / (5 * period))
        art += 0.3 * np.random.randn(len(t))
        return art
    
    def co2_waveform(self, t, period):
        co2 = np.zeros_like(t)
        etco2_peak = 40
        baseline = 0
        
        insp_dur = 0.5 * period
        exp_dur = 0.5 * period
        
        for i in range(len(t)):
            tau = t[i] % period
            
            if tau < insp_dur:
                time_in_insp = tau
                co2[i] = etco2_peak * np.exp(-time_in_insp / (0.3 * insp_dur)) + baseline
            else:
                time_in_exp = tau - insp_dur
                if time_in_exp < 0.1 * exp_dur:
                    co2[i] = baseline + etco2_peak * (1 - np.exp(-time_in_exp / (0.05 * exp_dur)))
                elif time_in_exp < 0.7 * exp_dur:
                    co2[i] = etco2_peak
                else:
                    time_from_plateau = time_in_exp - 0.7 * exp_dur
                    co2[i] = etco2_peak * np.exp(-time_from_plateau / (0.2 * exp_dur)) + baseline
        
        co2 += 1 * np.sin(2 * np.pi * t / period * 0.5)
        co2 += 0.3 * np.random.randn(len(t))
        return np.clip(co2, 0, 50)
    
    def compute_vitals(self, ecg, pleth, resp, art, co2, t):
        hr_str = "75"
        spo2_str = "98%"
        rr_str = "18"
        nibp_str = "120/80 (93)"
        temp_str = "37.0°C"
        etco2_str = "35 mmHg"

        return {
            'hr': hr_str,
            'spo2': spo2_str,
            'rr': rr_str,
            'nibp': nibp_str,
            'temp': temp_str,
            'co2': etco2_str
        }
