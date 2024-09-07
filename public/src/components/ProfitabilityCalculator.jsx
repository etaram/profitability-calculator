import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const ProfitabilityCalculator = () => {
  const [numVillas, setNumVillas] = useState(10);
  const [villaSize, setVillaSize] = useState(200);
  const [nightlyRate, setNightlyRate] = useState(3500);
  const [occupancyRate, setOccupancyRate] = useState(40);
  const [landCost, setLandCost] = useState(500000);
  const [minBuildCost, setMinBuildCost] = useState(8000);
  const [maxBuildCost, setMaxBuildCost] = useState(15000);
  const [minOperatingCost, setMinOperatingCost] = useState(4000);
  const [maxOperatingCost, setMaxOperatingCost] = useState(9500);
  const [marketingCost, setMarketingCost] = useState(600000);
  const [landDevelopmentCost, setLandDevelopmentCost] = useState(200000);
  const [publicAreaCost, setPublicAreaCost] = useState(1000000);
  const [receptionBuildingCost, setReceptionBuildingCost] = useState(700000);
  const [eventHallCost, setEventHallCost] = useState(700000);
  const [planningCost, setPlanningCost] = useState(150000);
  const [cleaningCostPerNight, setCleaningCostPerNight] = useState(200);
  const [amenitiesCostPerNight, setAmenitiesCostPerNight] = useState(50);
  const [maintenanceCostPerYear, setMaintenanceCostPerYear] = useState(20000);
  const [insuranceCostPerYear, setInsuranceCostPerYear] = useState(5000);
  const [propertyTaxRate, setPropertyTaxRate] = useState(1);
  const [inflationRate, setInflationRate] = useState(2);
  const [discountRate, setDiscountRate] = useState(8);
  const [primeRate, setPrimeRate] = useState(3.5);
  const [additionalInterestRate, setAdditionalInterestRate] = useState(1);

  const [results, setResults] = useState({
    totalInitialCostMin: 0,
    totalInitialCostMax: 0,
    annualRevenue: 0,
    profitMin: 0,
    profitMax: 0,
    roiMin: 0,
    roiMax: 0,
    npvMin: 0,
    npvMax: 0,
    irrMin: 0,
    irrMax: 0,
    paybackPeriodMin: 0,
    paybackPeriodMax: 0,
    yearlyData: []
  });

  const calculateProfitability = () => {
    // Calculate total initial cost, annual revenue, etc.
    const newResults = {
      totalInitialCostMin: numVillas * (landCost + villaSize * minBuildCost),
      totalInitialCostMax: numVillas * (landCost + villaSize * maxBuildCost),
      annualRevenue: numVillas * nightlyRate * (occupancyRate / 100) * 365,
      // Calculate other metrics like profit, ROI, NPV, IRR, payback period
      // Here you can use formulas to calculate these values based on the input parameters
    };

    // Return new results object
    return newResults;
  };

  useEffect(() => {
    const newResults = calculateProfitability();
    setResults(newResults);
  }, [numVillas, villaSize, nightlyRate, occupancyRate, landCost, minBuildCost, maxBuildCost, minOperatingCost, maxOperatingCost, marketingCost, landDevelopmentCost, publicAreaCost, receptionBuildingCost, eventHallCost, planningCost, cleaningCostPerNight, amenitiesCostPerNight, maintenanceCostPerYear, insuranceCostPerYear, propertyTaxRate, inflationRate, discountRate, primeRate, additionalInterestRate]);

  const renderInputField = (label, value, setter, step = 1) => (
    <div>
      <Label htmlFor={label}>{label}</Label>
      <Input 
        id={label} 
        type="number" 
        value={value} 
        onChange={(e) => setter(Number(e.target.value))}
        step={step}
      />
    </div>
  );

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">פאנל חישוב כדאיות דינמי לפרויקט וילות נופש</h1>

      <Tabs defaultValue="input" className="mt-4">
        <TabsList>
          <TabsTrigger value="input">פרמטרים</TabsTrigger>
          <TabsTrigger value="summary">סיכום תוצאות</TabsTrigger>
          <TabsTrigger value="detailed">ניתוח מפורט</TabsTrigger>
          <TabsTrigger value="graphs">גרפים</TabsTrigger>
        </TabsList>
        
        <TabsContent value="input">
          <Card>
            <CardHeader>פרמטרים לחישוב</CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4">
                {renderInputField("מספר וילות", numVillas, setNumVillas)}
                {renderInputField("גודל וילה (מ\"ר)", villaSize, setVillaSize)}
                {renderInputField("מחיר ללילה (₪)", nightlyRate, setNightlyRate)}
                {renderInputField("שיעור תפוסה (%)", occupancyRate, setOccupancyRate, 0.1)}
                {renderInputField("עלות קרקע לוילה (₪)", landCost, setLandCost)}
                {renderInputField("עלות בנייה מינימלית למ\"ר (₪)", minBuildCost, setMinBuildCost)}
                {renderInputField("עלות בנייה מקסימלית למ\"ר (₪)", maxBuildCost, setMaxBuildCost)}
                {renderInputField("עלות תפעול חודשית מינימלית לוילה (₪)", minOperatingCost, setMinOperatingCost)}
                {renderInputField("עלות תפעול חודשית מקסימלית לוילה (₪)", maxOperatingCost, setMaxOperatingCost)}
                {renderInputField("עלות שיווק שנתית (₪)", marketingCost, setMarketingCost)}
                {renderInputField("עלות פיתוח קרקע (₪)", landDevelopmentCost, setLandDevelopmentCost)}
                {renderInputField("עלות פיתוח שטח ציבורי וחניות (₪)", publicAreaCost, setPublicAreaCost)}
                {renderInputField("עלות מבנה קבלה ולוגיסטיקה (₪)", receptionBuildingCost, setReceptionBuildingCost)}
                {renderInputField("עלות אולם אירועים קטן (₪)", eventHallCost, setEventHallCost)}
                {renderInputField("עלות תכנון ויועצים (₪)", planningCost, setPlanningCost)}
                {renderInputField("עלות ניקיון ללילה (₪)", cleaningCostPerNight, setCleaningCostPerNight)}
                {renderInputField("עלות אביזרים ללילה (₪)", amenitiesCostPerNight, setAmenitiesCostPerNight)}
                {renderInputField("עלות תחזוקה שנתית לוילה (₪)", maintenanceCostPerYear, setMaintenanceCostPerYear)}
                {renderInputField("עלות ביטוח שנתית לוילה (₪)", insuranceCostPerYear, setInsuranceCostPerYear)}
                {renderInputField("שיעור מס רכוש שנתי (%)", propertyTaxRate, setPropertyTaxRate, 0.1)}
                {renderInputField("שיעור אינפלציה שנתי (%)", inflationRate, setInflationRate, 0.1)}
                {renderInputField("שיעור היוון (%)", discountRate, setDiscountRate, 0.1)}
                {renderInputField("ריבית פריים (%)", primeRate, setPrimeRate, 0.1)}
                {renderInputField("ריבית נוספת מעל הפריים (%)", additionalInterestRate, setAdditionalInterestRate, 0.1)}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="summary">
          <Card>
            <CardHeader>סיכום תוצאות</CardHeader>
            <CardContent>
              <p>השקעה ראשונית: ₪{results.totalInitialCostMin?.toLocaleString()} - ₪{results.totalInitialCostMax?.toLocaleString()}</p>
              <p>הכנסה שנתית: ₪{results.annualRevenue?.toLocaleString()}</p>
              <p>רווח שנתי: ₪{results.profitMin?.toLocaleString()} - ₪{results.profitMax?.toLocaleString()}</p>
              <p>תשואה על ההשקעה (ROI): {results.roiMin?.toFixed(2)}% - {results.roiMax?.toFixed(2)}%</p>
              <p>ערך נוכחי נקי (NPV): ₪{results.npvMin?.toLocaleString()} - ₪{results.npvMax?.toLocaleString()}</p>
              <p>שיעור תשואה פנימי (IRR): {results.irrMin?.toFixed(2)}% - {results.irrMax?.toFixed(2)}%</p>
              <p>תקופת החזר השקעה: {results.paybackPeriodMin?.toFixed(2)} - {results.paybackPeriodMax?.toFixed(2)} שנים</p>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="detailed">
          <Card>
            <CardHeader>ניתוח מפורט</CardHeader>
            <CardContent>
              {/* Add detailed analysis content here */}
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="graphs">
          <Card>
            <CardHeader>ניתוח גרפי</CardHeader>
            <CardContent>
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={results.yearlyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="revenue" name="הכנסה" stroke="#8884d8" />
                    <Line type="monotone" dataKey="costsMin" name="עלויות (מינימום)" stroke="#82ca9d" />
                    <Line type="monotone" dataKey="costsMax" name="עלויות (מקסימום)" stroke="#ffc658" />
                    <Line type="monotone" dataKey="profitMin" name="רווח (מינימום)" stroke="#ff7300" />
                    <Line type="monotone" dataKey="profitMax" name="רווח (מקסימום)" stroke="#ff0000" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ProfitabilityCalculator;
