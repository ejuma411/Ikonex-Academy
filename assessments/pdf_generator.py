from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from datetime import datetime


class ProfessionalReportPDF:
    """Professional school report generator using ReportLab"""
    
    def __init__(self, buffer, class_stream, ranking, subjects, stats):
        self.buffer = buffer
        self.class_stream = class_stream
        self.ranking = ranking
        self.subjects = subjects
        self.stats = stats
        self.styles = self._create_styles()
    
    def _create_styles(self):
        """Create professional paragraph styles"""
        styles = getSampleStyleSheet()
        
        # Custom styles
        styles.add(ParagraphStyle(
            name='SchoolTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=colors.HexColor('#1a4d8c'),
            alignment=TA_CENTER,
            spaceAfter=6
        ))
        
        styles.add(ParagraphStyle(
            name='SchoolSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=colors.HexColor('#1a4d8c'),
            alignment=TA_CENTER,
            spaceAfter=10
        ))
        
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            spaceBefore=12
        ))
        
        styles.add(ParagraphStyle(
            name='TableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            alignment=TA_LEFT
        ))
        
        styles.add(ParagraphStyle(
            name='TableCellCenter',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            alignment=TA_CENTER
        ))
        
        styles.add(ParagraphStyle(
            name='TableCellBold',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            alignment=TA_CENTER
        ))
        
        return styles
    
    def _header(self, canvas, doc):
        """Draw header on each page"""
        canvas.saveState()
        # School name header
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(colors.HexColor('#1a4d8c'))
        canvas.drawString(1.5*cm, A4[1] - 1*cm, "IKONEX ACADEMY")
        
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(colors.HexColor('#666666'))
        canvas.drawString(1.5*cm, A4[1] - 1.3*cm, "Excellence in Education")
        
        # Line separator
        canvas.setStrokeColor(colors.HexColor('#1a4d8c'))
        canvas.setLineWidth(1)
        canvas.line(1.5*cm, A4[1] - 1.6*cm, A4[0] - 1.5*cm, A4[1] - 1.6*cm)
        
        canvas.restoreState()
    
    def _footer(self, canvas, doc):
        """Draw footer on each page"""
        canvas.saveState()
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(colors.HexColor('#888888'))
        canvas.drawString(1.5*cm, 1*cm, f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        canvas.drawRightString(A4[0] - 1.5*cm, 1*cm, f"Page {doc.page}")
        canvas.restoreState()
    
    def generate(self):
      """Generate the complete PDF report"""
      doc = SimpleDocTemplate(
         self.buffer,
         pagesize=A4,
         topMargin=2.5*cm,
         bottomMargin=2*cm,
         leftMargin=1.5*cm,
         rightMargin=1.5*cm
      )
      
      story = []
      
      # ===== HEADER SECTION =====
      story.append(Paragraph("IKONEX ACADEMY", self.styles['SchoolTitle']))
      story.append(Paragraph("EXCELLENCE IN EDUCATION", self.styles['SchoolSubtitle']))
      story.append(Spacer(1, 5))
      story.append(Paragraph("ACADEMIC PERFORMANCE REPORT", self.styles['ReportTitle']))
      story.append(Spacer(1, 15))
      
      # ===== CLASS INFORMATION TABLE =====
      class_info_data = [
         [Paragraph("<b>Class Stream:</b>", self.styles['TableCell']), 
            Paragraph(self.class_stream.name, self.styles['TableCellBold'])],
         [Paragraph("<b>Academic Year:</b>", self.styles['TableCell']), 
            Paragraph(f"{datetime.now().year}/{datetime.now().year + 1}", self.styles['TableCell'])],
         [Paragraph("<b>Term:</b>", self.styles['TableCell']), 
            Paragraph("Term 2", self.styles['TableCell'])],
         [Paragraph("<b>Report Date:</b>", self.styles['TableCell']), 
            Paragraph(datetime.now().strftime("%d/%m/%Y"), self.styles['TableCell'])],
      ]
      
      class_info_table = Table(class_info_data, colWidths=[4*cm, 8*cm])
      class_info_table.setStyle(TableStyle([
         ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
         ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
         ('TOPPADDING', (0, 0), (-1, -1), 6),
         ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
         ('LEFTPADDING', (0, 0), (-1, -1), 8),
      ]))
      story.append(class_info_table)
      story.append(Spacer(1, 20))
      
      # ===== STATISTICS CARDS =====
      stats_data = [
         [
               Paragraph(f"<font size='16'><b>{self.stats['total_students']}</b></font><br/><font size='8'>Total Students</font>", self.styles['TableCellCenter']),
               Paragraph(f"<font size='16'><b>{self.stats['class_average']}%</b></font><br/><font size='8'>Class Average</font>", self.styles['TableCellCenter']),
               Paragraph(f"<font size='16'><b>{self.stats['highest_score']}</b></font><br/><font size='8'>Highest Score</font>", self.styles['TableCellCenter']),
               Paragraph(f"<font size='16'><b>{self.stats['pass_count']}/{self.stats['total_students']}</b></font><br/><font size='8'>Proficiency Rate</font>", self.styles['TableCellCenter']),
         ]
      ]
      
      stats_table = Table(stats_data, colWidths=[4.25*cm, 4.25*cm, 4.25*cm, 4.25*cm])
      stats_table.setStyle(TableStyle([
         ('BACKGROUND', (0, 0), (-1, -1), colors.white),
         ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
         ('TOPPADDING', (0, 0), (-1, -1), 10),
         ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
      ]))
      story.append(stats_table)
      story.append(Spacer(1, 20))
      
      # ===== SUBJECTS SECTION =====
      if self.subjects:
         story.append(Paragraph("SUBJECT ANALYSIS", self.styles['SectionHeader']))
         story.append(Spacer(1, 5))
         
         # FIXED: Use 'sub.subject.name' instead of 'sub.class_subject.subject.name'
         subject_list = [[Paragraph(sub.subject.name, self.styles['TableCell'])] for sub in self.subjects[:10]]
         if subject_list:
               subjects_table = Table(subject_list, colWidths=[6*cm])
               subjects_table.setStyle(TableStyle([
                  ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
                  ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                  ('TOPPADDING', (0, 0), (-1, -1), 6),
                  ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                  ('LEFTPADDING', (0, 0), (-1, -1), 10),
               ]))
               story.append(subjects_table)
               story.append(Spacer(1, 15))
      
      # ===== RANKING TABLE =====
      story.append(Paragraph("STUDENT RANKING & PERFORMANCE", self.styles['SectionHeader']))
      story.append(Spacer(1, 5))
      
      # Table headers
      ranking_data = [
         ['RANK', 'STUDENT NAME', 'ADMISSION NO', 'TOTAL', 'AVG %', 'GRADE', 'REMARK']
      ]
      
      # Add student data
      for item in self.ranking:
         # Determine remark based on grade
         grade = item['grade']
         if grade in ['A', 'A-']:
               remark = 'Excellent'
         elif grade in ['B+', 'B', 'B-']:
               remark = 'Good'
         elif grade in ['C+', 'C', 'C-']:
               remark = 'Satisfactory'
         elif grade in ['D+', 'D', 'D-']:
               remark = 'Below Average'
         else:
               remark = 'Needs Improvement'
         
         ranking_data.append([
               f"{item['position']}{'st' if item['position'] == 1 else 'nd' if item['position'] == 2 else 'rd' if item['position'] == 3 else 'th'}",
               f"{item['student'].first_name} {item['student'].last_name}",
               item['student'].admission_no or '-',
               f"{item['total']:.1f}",
               f"{item['average']:.1f}%",
               item['grade'] or 'N/A',
               remark
         ])
      
      # Create table with proper column widths
      col_widths = [1.2*cm, 4.5*cm, 2.5*cm, 1.8*cm, 1.8*cm, 1.5*cm, 2.5*cm]
      ranking_table = Table(ranking_data, colWidths=col_widths, repeatRows=1)
      
      # Style the table
      ranking_table.setStyle(TableStyle([
         # Header row
         ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d8c')),
         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
         ('FONTSIZE', (0, 0), (-1, 0), 8),
         ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
         ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
         ('TOPPADDING', (0, 0), (-1, 0), 8),
         ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
         
         # Body rows
         ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
         ('FONTSIZE', (0, 1), (-1, -1), 8),
         ('ALIGN', (1, 1), (1, -1), 'LEFT'),
         ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
         ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
         ('TOPPADDING', (0, 1), (-1, -1), 6),
         ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
         ('LEFTPADDING', (0, 1), (-1, -1), 4),
         ('RIGHTPADDING', (0, 1), (-1, -1), 4),
         
         # Grid lines
         ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
         
         # Alternating row colors
         ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
      ]))
      
      story.append(ranking_table)
      story.append(Spacer(1, 30))
      
      # ===== SIGNATURES =====
      sig_data = [
         ['', '', ''],
         ['_________________', '_________________', '_________________'],
         ['Class Teacher', 'Principal / Head of School', 'Date']
      ]
      sig_table = Table(sig_data, colWidths=[5*cm, 5*cm, 5*cm])
      sig_table.setStyle(TableStyle([
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
         ('TOPPADDING', (0, 0), (-1, -1), 10),
         ('FONTSIZE', (0, 0), (-1, -1), 8),
      ]))
      story.append(sig_table)
      
      # Combined header and footer function
      def header_and_footer(canvas, doc):
         self._header(canvas, doc)
         self._footer(canvas, doc)
      
      # Build PDF
      doc.build(story, onFirstPage=header_and_footer, onLaterPages=header_and_footer)
      
      return self.buffer     
      
class StudentReportPDF:
    """Professional student report generator using ReportLab"""
    
    def __init__(self, buffer, student, scores, subject_summary, total, average, grade, class_position, class_size):
        self.buffer = buffer
        self.student = student
        self.scores = scores
        self.subject_summary = subject_summary
        self.total = total
        self.average = average
        self.grade = grade
        self.class_position = class_position
        self.class_size = class_size
        self.styles = self._create_styles()
    
    def _create_styles(self):
        """Create professional paragraph styles"""
        styles = getSampleStyleSheet()
        
        styles.add(ParagraphStyle(
            name='SchoolTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=colors.HexColor('#1a4d8c'),
            alignment=TA_CENTER,
            spaceAfter=6
        ))
        
        styles.add(ParagraphStyle(
            name='SchoolSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=colors.HexColor('#1a4d8c'),
            alignment=TA_CENTER,
            spaceAfter=10
        ))
        
        styles.add(ParagraphStyle(
            name='StudentName',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=colors.HexColor('#1a4d8c'),
            alignment=TA_CENTER,
            spaceAfter=5
        ))
        
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            spaceBefore=12
        ))
        
        styles.add(ParagraphStyle(
            name='TableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            alignment=TA_LEFT
        ))
        
        styles.add(ParagraphStyle(
            name='TableCellCenter',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            alignment=TA_CENTER
        ))
        
        styles.add(ParagraphStyle(
            name='TableCellBold',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            alignment=TA_CENTER
        ))
        
        return styles
    
    def _header(self, canvas, doc):
        """Draw header on each page"""
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(colors.HexColor('#1a4d8c'))
        canvas.drawString(1.5*cm, A4[1] - 1*cm, "IKONEX ACADEMY")
        
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(colors.HexColor('#666666'))
        canvas.drawString(1.5*cm, A4[1] - 1.3*cm, "Excellence in Education")
        
        canvas.setStrokeColor(colors.HexColor('#1a4d8c'))
        canvas.setLineWidth(1)
        canvas.line(1.5*cm, A4[1] - 1.6*cm, A4[0] - 1.5*cm, A4[1] - 1.6*cm)
        
        canvas.restoreState()
    
    def _footer(self, canvas, doc):
        """Draw footer on each page"""
        canvas.saveState()
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(colors.HexColor('#888888'))
        canvas.drawString(1.5*cm, 1*cm, f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        canvas.drawRightString(A4[0] - 1.5*cm, 1*cm, f"Page {doc.page}")
        canvas.restoreState()
    
    def generate(self):
        """Generate the complete student PDF report"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            topMargin=2.5*cm,
            bottomMargin=2*cm,
            leftMargin=1.5*cm,
            rightMargin=1.5*cm
        )
        
        story = []
        
        # ===== HEADER SECTION =====
        story.append(Paragraph("IKONEX ACADEMY", self.styles['SchoolTitle']))
        story.append(Paragraph("EXCELLENCE IN EDUCATION", self.styles['SchoolSubtitle']))
        story.append(Spacer(1, 5))
        story.append(Paragraph("STUDENT PERFORMANCE REPORT", self.styles['ReportTitle']))
        story.append(Spacer(1, 15))
        
        # ===== STUDENT NAME =====
        story.append(Paragraph(f"{self.student.first_name} {self.student.last_name}", self.styles['StudentName']))
        story.append(Spacer(1, 10))
        
        # ===== STUDENT INFORMATION TABLE =====
        student_info_data = [
            [Paragraph("<b>Admission No:</b>", self.styles['TableCell']), 
             Paragraph(self.student.admission_no or 'Not Assigned', self.styles['TableCell'])],
            [Paragraph("<b>Class Stream:</b>", self.styles['TableCell']), 
             Paragraph(self.student.class_stream.name if self.student.class_stream else 'Not Assigned', self.styles['TableCell'])],
            [Paragraph("<b>Position:</b>", self.styles['TableCell']), 
             Paragraph(f"{self.class_position} of {self.class_size}", self.styles['TableCell'])],
            [Paragraph("<b>Report Date:</b>", self.styles['TableCell']), 
             Paragraph(datetime.now().strftime("%d/%m/%Y"), self.styles['TableCell'])],
        ]
        
        student_info_table = Table(student_info_data, colWidths=[4*cm, 8*cm])
        student_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(student_info_table)
        story.append(Spacer(1, 20))
        
        # ===== PERFORMANCE STATS CARDS =====
        stats_data = [
            [
                Paragraph(f"<font size='16'><b>{self.total}</b></font><br/><font size='8'>Total Marks</font>", self.styles['TableCellCenter']),
                Paragraph(f"<font size='16'><b>{self.average}%</b></font><br/><font size='8'>Average</font>", self.styles['TableCellCenter']),
                Paragraph(f"<font size='16'><b>{self.grade}</b></font><br/><font size='8'>Grade</font>", self.styles['TableCellCenter']),
                Paragraph(f"<font size='16'><b>{self.class_position}</b></font><br/><font size='8'>Class Position</font>", self.styles['TableCellCenter']),
            ]
        ]
        
        stats_table = Table(stats_data, colWidths=[4.25*cm, 4.25*cm, 4.25*cm, 4.25*cm])
        
        # Determine grade color for the grade card
        grade_color = colors.HexColor('#15803d')  # green for A
        if self.grade and self.grade.startswith('B'):
            grade_color = colors.HexColor('#1e40af')  # blue for B
        elif self.grade and self.grade.startswith('C'):
            grade_color = colors.HexColor('#854d0e')  # yellow for C
        elif self.grade and self.grade.startswith('D'):
            grade_color = colors.HexColor('#9a3412')  # orange for D
        elif self.grade in ['E', 'F']:
            grade_color = colors.HexColor('#b91c1c')  # red for E/F
        
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (2, 0), (2, 0), grade_color),
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 20))
        
        # ===== SUBJECT SUMMARY TABLE =====
        story.append(Paragraph("SUBJECT PERFORMANCE SUMMARY", self.styles['SectionHeader']))
        story.append(Spacer(1, 5))
        
        # Table headers
        subject_data = [
            ['SUBJECT', 'TOTAL MARKS', 'AVERAGE', 'GRADE', 'REMARK']
        ]
        
        # Add subject data
        for item in self.subject_summary:
            # Determine remark based on grade
            grade = item.get('grade', 'N/A')
            if grade in ['A', 'A-']:
                remark = 'Excellent'
            elif grade in ['B+', 'B', 'B-']:
                remark = 'Good'
            elif grade in ['C+', 'C', 'C-']:
                remark = 'Satisfactory'
            elif grade in ['D+', 'D', 'D-']:
                remark = 'Below Average'
            else:
                remark = 'Needs Improvement'
            
            subject_data.append([
                item.get('subject_name', 'N/A'),
                f"{item.get('total', 0):.1f}",
                f"{item.get('average', 0):.1f}%",
                grade,
                remark
            ])
        
        subject_table = Table(subject_data, colWidths=[5*cm, 2.5*cm, 2.5*cm, 1.5*cm, 3.5*cm], repeatRows=1)
        subject_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d8c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Body rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (1, 1), (2, -1), 'CENTER'),
            ('ALIGN', (3, 1), (4, -1), 'CENTER'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 1), (-1, -1), 6),
            ('RIGHTPADDING', (0, 1), (-1, -1), 6),
            
            # Grid lines
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        
        story.append(subject_table)
        story.append(Spacer(1, 20))
        
        # ===== ASSESSMENT SCORES TABLE =====
        if self.scores:
            story.append(Paragraph("ASSESSMENT SCORE BREAKDOWN", self.styles['SectionHeader']))
            story.append(Spacer(1, 5))
            
            scores_data = [
                ['ASSESSMENT', 'SUBJECT', 'MARKS']
            ]
            
            for score in self.scores:
                scores_data.append([
                    score.assessment.name,
                    score.subject.name,
                    f"{score.marks}"
                ])
            
            scores_table = Table(scores_data, colWidths=[6*cm, 6*cm, 3*cm], repeatRows=1)
            scores_table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d8c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                
                # Body rows
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('LEFTPADDING', (0, 1), (-1, -1), 6),
                ('RIGHTPADDING', (0, 1), (-1, -1), 6),
                
                # Grid lines
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                
                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ]))
            
            story.append(scores_table)
            story.append(Spacer(1, 20))
        
        # ===== SIGNATURES =====
        sig_data = [
            ['', '', ''],
            ['_________________', '_________________', '_________________'],
            ['Class Teacher', 'Principal / Head of School', 'Parent/Guardian']
        ]
        sig_table = Table(sig_data, colWidths=[5*cm, 5*cm, 5*cm])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(sig_table)
        
        # Combined header and footer function
        def header_and_footer(canvas, doc):
            self._header(canvas, doc)
            self._footer(canvas, doc)
        
        # Build PDF
        doc.build(story, onFirstPage=header_and_footer, onLaterPages=header_and_footer)
        
        return self.buffer      
      
