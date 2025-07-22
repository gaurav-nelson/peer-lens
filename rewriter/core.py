"""
AI Rewriter Core Module
Uses Assembly Line approach exclusively for surgical precision.
"""

import logging
import time
from typing import Dict, List, Any, Optional, Callable

from .models import ModelManager
from .generators import TextGenerator  
from .processors import TextProcessor
from .evaluators import RewriteEvaluator
from .assembly_line_rewriter import AssemblyLineRewriter

logger = logging.getLogger(__name__)


class AIRewriter:
    """AI-powered text rewriter with assembly line precision."""
    
    def __init__(self, use_ollama: bool = True, ollama_model: str = "llama3:8b", 
                 progress_callback: Optional[Callable] = None):
        """Initialize the AI rewriter with assembly line capability."""
        self.progress_callback = progress_callback
        
        # Initialize components
        self.model_manager = ModelManager(use_ollama, ollama_model)
        self.text_generator = TextGenerator(self.model_manager)
        self.text_processor = TextProcessor()
        self.evaluator = RewriteEvaluator()
        
        # Initialize assembly line rewriter (ONLY approach now)
        self.assembly_line = AssemblyLineRewriter(
            self.text_generator, 
            self.text_processor, 
            progress_callback
        )
        
        logger.info("AIRewriter initialized - Assembly Line ONLY approach")
    
    def rewrite(self, content: str, errors: List[Dict[str, Any]], 
                context: str = "sentence", pass_number: int = 1) -> Dict[str, Any]:
        """
        Generate AI-powered rewrite suggestions using assembly line approach.
        
        Args:
            content: Original text content
            errors: List of detected errors
            context: Context level ('sentence' or 'paragraph')
            pass_number: 1 for initial rewrite, 2 for refinement
            
        Returns:
            Dictionary with rewrite results
        """
        try:
            if not content or not content.strip():
                return {
                    'rewritten_text': '',
                    'improvements': [],
                    'confidence': 0.0,
                    'error': 'No content provided'
                }
            
            if not errors and pass_number == 1:
                return {
                    'rewritten_text': content,
                    'improvements': ['No errors detected'],
                    'confidence': 1.0
                }
            
            # Check if AI models are available
            if not self.text_generator.is_available():
                return {
                    'rewritten_text': content,
                    'improvements': [],
                    'confidence': 0.0,
                    'error': 'AI models are not available. Please check your model configuration.'
                }
            
            # Use assembly line for BOTH passes
            if pass_number == 1:
                return self._perform_assembly_line_pass(content, errors, context)
            else:
                return self._perform_assembly_line_refinement(content, errors, context)
            
        except Exception as e:
            logger.error(f"Error in rewrite: {str(e)}")
            return {
                'rewritten_text': content,
                'improvements': [],
                'confidence': 0.0,
                'error': f'AI rewrite failed: {str(e)}'
            }
    
    def _perform_assembly_line_pass(self, content: str, errors: List[Dict[str, Any]], context: str) -> Dict[str, Any]:
        """Perform assembly line rewriting with sequential error fixing."""
        logger.info("🏭 Starting Assembly Line Rewriting (Pass 1)")
        logger.info(f"📊 Processing {len(errors)} errors with surgical precision")
        
        if self.progress_callback:
            self.progress_callback('assembly_start', 'Assembly Line: Starting precision rewriting...', 
                                 'Organizing errors by priority', 10)
        
        # Apply assembly line fixes
        result = self.assembly_line.apply_assembly_line_fixes(content, errors, context)
        
        if result.get('assembly_line_used'):
            # Evaluate improvements made
            improvements = self.evaluator.extract_improvements(content, result['rewritten_text'])
            if improvements:
                result['improvements'] = improvements
            
            # Add pass metadata
            result['pass_number'] = 1
            result['can_refine'] = True
            result['model_used'] = f"{self.model_manager.ollama_model if self.model_manager.use_ollama else 'hf_transformers'}"
            
            logger.info(f"✅ Assembly Line Pass 1 complete: {result.get('errors_fixed', 0)}/{result.get('original_errors', 0)} errors fixed")
            
            if self.progress_callback:
                self.progress_callback('assembly_complete', 'Assembly Line: Precision rewriting completed!', 
                                     f"Fixed {result.get('errors_fixed', 0)} errors with surgical precision", 100)
        
        return result
    
    def _perform_assembly_line_refinement(self, content: str, errors: List[Dict[str, Any]], context: str) -> Dict[str, Any]:
        """Perform assembly line refinement (Pass 2) - re-analyze and fix remaining issues."""
        logger.info("🔍 Starting Assembly Line Refinement (Pass 2)")
        logger.info("🔄 Re-analyzing content for any remaining issues...")
        
        if self.progress_callback:
            self.progress_callback('pass2_start', 'Assembly Line Refinement: Re-analyzing content...', 
                                 'Detecting any remaining style issues', 20)
        
        # For refinement, we could:
        # 1. Re-run analysis on the refined content to find new errors
        # 2. Or use a "refinement mode" that focuses on polish
        # For now, let's run the assembly line again with any errors passed in
        
        result = self.assembly_line.apply_assembly_line_fixes(content, errors, context)
        
        if result.get('assembly_line_used'):
            # Evaluate refinement improvements
            improvements = self.evaluator.extract_improvements(content, result['rewritten_text'])
            if improvements:
                result['improvements'] = improvements
            
            # Add refinement pass metadata
            result['pass_number'] = 2
            result['can_refine'] = False  # No third pass
            result['model_used'] = f"{self.model_manager.ollama_model if self.model_manager.use_ollama else 'hf_transformers'}"
            
            logger.info(f"✅ Assembly Line Refinement complete: {result.get('errors_fixed', 0)} additional fixes applied")
            
            if self.progress_callback:
                self.progress_callback('pass2_complete', 'Assembly Line Refinement: Completed!', 
                                     f"Applied {result.get('errors_fixed', 0)} refinement fixes", 100)
        
        return result
    
    def refine(self, content: str, errors: List[Dict[str, Any]], context: str = "sentence") -> Dict[str, Any]:
        """
        Perform refinement using assembly line approach.
        This is a convenience method that calls rewrite with pass_number=2.
        """
        return self.rewrite(content, errors, context, pass_number=2)
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information."""
        return {
            'ai_available': self.text_generator.is_available(),
            'assembly_line_enabled': True, # Always true with this new approach
            'model_info': {
                'use_ollama': self.model_manager.use_ollama,
                'ollama_model': self.model_manager.ollama_model,
                'ollama_available': self.model_manager.is_ollama_available()
            },
            'capabilities': {
                'assembly_line_rewriting': True,
                'legacy_rewriting': False, # No legacy rewriting
                'two_pass_refinement': False, # No two-pass refinement
                'error_validation': True
            }
        } 